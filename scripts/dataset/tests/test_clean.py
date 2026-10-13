"""Tests for check_raw.check() and clean.py (Phase 3).

All rows are synthetic and built in a temporary file (ADR 0005 §3, ADR 0011):
no real posting text is used. Run from the repository root:
    py -3.13 -m unittest discover -s scripts/dataset/tests -v
"""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # scripts/dataset/

import clean  # noqa: E402
from check_raw import TEMPLATE, check  # noqa: E402

with TEMPLATE.open(encoding="utf-8", newline="") as _f:
    COLUMNS = next(csv.reader(_f))


def posting(ref: str, **values: str) -> dict[str, str]:
    """A valid synthetic row; keyword arguments override single columns."""
    row = dict.fromkeys(COLUMNS, "")
    row.update(posting_ref=ref, source="JobsDB", source_url=f"https://th.jobsdb.com/job/{ref[3:]}",
               search_keyword="frontend developer", date_collected="2026-10-01",
               job_title="Front-end Developer", company="Example Co., Ltd.",
               requirements="- Experience with HTML and CSS")
    row.update(values)
    return row


class RawFileCase(unittest.TestCase):
    """Writes rows to a temporary CSV (CRLF, UTF-8 like the Google Sheet export)."""

    def write(self, rows: list[dict[str, str]]) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "job_postings.csv"
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\r\n")
            w.writeheader()
            w.writerows(rows)
        return path


class CleanTextTest(unittest.TestCase):
    def test_keeps_line_breaks_and_tidies_bullets_spaces_and_blank_lines(self):
        raw = "Required:\r\n•  HTML​   and CSS  \r\n\r\n\r\n● React\r\nBonus:\nGit\t "
        self.assertEqual(clean.clean_text(raw), "Required:\n- HTML and CSS\n\n- React\nBonus:\n- Git")

    def test_hyphen_bullets_and_plain_text_are_unchanged(self):
        self.assertEqual(clean.clean_text("- HTML\n- CSS"), "- HTML\n- CSS")
        self.assertEqual(clean.clean_text("ใช้ React ได้"), "ใช้ React ได้")

    def test_empty_text_stays_empty(self):
        self.assertEqual(clean.clean_text(" \r\n \n"), "")

    def test_clean_line_joins_lines_and_spaces(self):
        self.assertEqual(clean.clean_line("  Senior \n Full Stack Developer "), "Senior Full Stack Developer")


class CanonicalUrlTest(unittest.TestCase):
    def test_jobsdb_drops_query_and_language_prefix(self):
        for url in ("https://th.jobsdb.com/job/123?type=standard&ref=search",
                    "https://th.jobsdb.com/th/job/123", "https://TH.jobsdb.com/job/123/#apply"):
            self.assertEqual(clean.canonical_url(url, "JobsDB"), "https://th.jobsdb.com/job/123")

    def test_jobthai_drops_tracking_parameters(self):
        self.assertEqual(clean.canonical_url("https://www.jobthai.com/th/job/456?utm_source=x&utm_medium=y", "JobThai"),
                         "https://www.jobthai.com/th/job/456")

    def test_unknown_shape_or_wrong_source_is_an_error(self):
        with self.assertRaises(ValueError):
            clean.canonical_url("https://th.jobsdb.com/companies/123", "JobsDB")
        with self.assertRaises(ValueError):
            clean.canonical_url("https://th.jobsdb.com/job/123", "JobThai")
        with self.assertRaises(ValueError):
            clean.canonical_url("https://example.com/job/1", "Other")


class LocationAndEmploymentTest(unittest.TestCase):
    MAP = {"bangkok": "Bangkok", "กรุงเทพมหานคร": "Bangkok", "chonburi": "Chon Buri"}

    def test_thai_and_english_names_map_to_one_province(self):
        self.assertEqual(clean.parse_location("กรุงเทพมหานคร", self.MAP), ("Bangkok", ""))
        self.assertEqual(clean.parse_location("Bangkok\n", self.MAP), ("Bangkok", ""))

    def test_work_mode_is_split_from_the_place(self):
        self.assertEqual(clean.parse_location("Bangkok (Hybrid)", self.MAP), ("Bangkok", "Hybrid"))
        self.assertEqual(clean.parse_location("Chonburi (On-site)", self.MAP), ("Chon Buri", "Onsite"))
        self.assertEqual(clean.parse_location("Remote", self.MAP), ("", "Remote"))

    def test_not_stated_stays_empty_and_unknown_place_is_an_error(self):
        self.assertEqual(clean.parse_location("", self.MAP), ("", ""))
        with self.assertRaises(KeyError):
            clean.parse_location("Atlantis", self.MAP)

    def test_employment_type(self):
        self.assertEqual(clean.employment_type("Full time\n"), "Full-time")
        self.assertEqual(clean.employment_type("Contract/Temp"), "Contract")
        self.assertEqual(clean.employment_type(""), "")
        with self.assertRaises(KeyError):
            clean.employment_type("Volunteer")

    def test_committed_location_map_covers_its_own_keys(self):
        location_map = clean.load_location_map()
        self.assertEqual(location_map["กรุงเทพมหานคร"], "Bangkok")
        self.assertEqual(location_map["chonburi"], location_map["ชลบุรี"])


class CleanFileTest(RawFileCase):
    def test_cleans_active_rows_and_lists_excluded_ones(self):
        path = self.write([
            posting("JP-0001", source_url="https://th.jobsdb.com/th/job/1?ref=search",
                    location="กรุงเทพมหานคร", employment_type="Full time",
                    requirements="• HTML\r\n\r\n\r\n• CSS"),
            posting("JP-0002", source="JobThai", source_url="https://www.jobthai.com/th/job/2?utm_source=x",
                    location="Bangkok (Hybrid)", employment_type="Contract/Temp"),
            posting("JP-0003", notes="exclude: out of scope (mobile only)"),
        ])
        result = clean.clean_file(path)
        self.assertEqual(result.errors, [])
        self.assertEqual([p["posting_ref"] for p in result.postings], ["JP-0001", "JP-0002"])
        self.assertEqual(result.excluded, [("JP-0003", "out of scope (mobile only)")])
        first, second = result.postings
        self.assertEqual(first["source_url"], "https://th.jobsdb.com/job/1")
        self.assertEqual(first["requirements"], "- HTML\n\n- CSS")
        self.assertEqual((first["location"], first["work_mode"], first["employment_type"]),
                         ("Bangkok", "", "Full-time"))
        self.assertEqual((second["location"], second["work_mode"], second["employment_type"]),
                         ("Bangkok", "Hybrid", "Contract"))

    def test_unknown_location_or_url_is_reported_per_posting(self):
        path = self.write([posting("JP-0001", location="Atlantis"),
                           posting("JP-0002", source_url="https://th.jobsdb.com/companies/2")])
        errors = "\n".join(clean.clean_file(path).errors)
        self.assertIn("JP-0001   location 'Atlantis'", errors)
        self.assertIn("JP-0002   source_url does not look like a JobsDB job page", errors)

    def test_raw_errors_stop_cleaning(self):
        path = self.write([posting("JP-0001", company="")])
        result = clean.clean_file(path)
        self.assertEqual(result.postings, [])
        self.assertIn("raw file has errors", result.errors[0])


class RefGapTest(RawFileCase):
    def test_gap_is_a_warning_unless_listed_as_unused(self):
        path = self.write([posting("JP-0001"), posting("JP-0003")])
        result = check(path, unused_refs={})
        self.assertEqual(result.errors, [])
        self.assertTrue(any(w.startswith("JP-0002") and "missing" in w for w in result.warnings))
        result = check(path, unused_refs={"JP-0002": "number skipped"})
        self.assertFalse(any("missing" in w for w in result.warnings))

    def test_listed_ref_that_exists_is_a_warning(self):
        path = self.write([posting("JP-0001")])
        result = check(path, unused_refs={"JP-0001": "number skipped"})
        self.assertTrue(any("listed in jobs/unused_refs.csv" in w for w in result.warnings))


if __name__ == "__main__":
    unittest.main()
