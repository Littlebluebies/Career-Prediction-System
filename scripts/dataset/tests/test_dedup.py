"""Tests for dedup.py (Phase 3). Synthetic postings only (ADR 0005 §3, ADR 0011).

Run from the repository root:
    py -3.13 -m unittest discover -s scripts/dataset/tests -v
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # scripts/dataset/

import dedup  # noqa: E402
from test_clean import RawFileCase, posting  # noqa: E402

SHARED = ("- Build web pages with React and TypeScript\n- Write REST APIs with Node.js and PostgreSQL\n"
          "- Review pull requests and write unit tests\n- Work with designers on responsive layouts")
OTHER = ("- Maintain the company ERP and write SQL reports\n- Support users and train new staff\n"
         "- Prepare monthly hardware inventory and printer maintenance")


def cleaned(ref: str, requirements: str, responsibilities: str = "", **values: str) -> dict[str, str]:
    """A posting as clean.py returns it (only the columns dedup reads)."""
    p = {"posting_ref": ref, "source": "JobsDB", "source_url": f"https://th.jobsdb.com/job/{ref[3:]}",
         "requirements": requirements, "responsibilities": responsibilities, "description": ""}
    p.update(values)
    return p


def review(*rows: tuple[str, str, str]) -> dict[tuple[str, str], dict[str, str]]:
    return {(a, b): {"posting_ref": a, "other_ref": b, "decision": d, "similarity": "", "reason": f"test {d}"}
            for a, b, d in rows}


class FindCandidatesTest(unittest.TestCase):
    def test_similar_text_is_a_candidate_and_unrelated_text_is_not(self):
        found = dedup.find_candidates([cleaned("JP-0001", SHARED), cleaned("JP-0002", SHARED + "\n- Git"),
                                       cleaned("JP-0003", OTHER)])
        self.assertEqual([(c.posting_ref, c.other_ref) for c in found], [("JP-0001", "JP-0002")])
        self.assertGreater(found[0].similarity, 0.9)

    def test_identical_long_column_is_a_candidate_even_when_the_rest_differs(self):
        found = dedup.find_candidates([cleaned("JP-0001", SHARED, responsibilities=OTHER * 3),
                                       cleaned("JP-0002", "- Figma", responsibilities=OTHER * 3)])
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].identical, ["responsibilities"])

    def test_rows_split_from_one_posting_are_never_candidates(self):
        url = "https://th.jobsdb.com/job/9"
        found = dedup.find_candidates([cleaned("JP-0001", SHARED, source_url=url),
                                       cleaned("JP-0002", SHARED, source_url=url)])
        self.assertEqual(found, [])

    def test_cross_source_pair_is_found(self):
        found = dedup.find_candidates([cleaned("JP-0001", SHARED),
                                       cleaned("JP-0002", SHARED, source="JobThai",
                                               source_url="https://www.jobthai.com/th/job/2")])
        self.assertEqual(found[0].sources, ("JobsDB", "JobThai"))


class DedupPostingsTest(unittest.TestCase):
    POSTINGS = [cleaned("JP-0001", SHARED), cleaned("JP-0002", SHARED), cleaned("JP-0003", SHARED),
                cleaned("JP-0004", OTHER)]

    def test_duplicate_group_keeps_the_lowest_ref(self):
        result = dedup.dedup_postings(self.POSTINGS, review(("JP-0001", "JP-0002", "duplicate"),
                                                            ("JP-0001", "JP-0003", "duplicate"),
                                                            ("JP-0002", "JP-0003", "duplicate")))
        self.assertEqual([p["posting_ref"] for p in result.postings], ["JP-0001", "JP-0004"])
        self.assertEqual([(r, of) for r, of, _ in result.duplicates], [("JP-0002", "JP-0001"), ("JP-0003", "JP-0001")])
        self.assertEqual((result.unreviewed, result.errors), ([], []))

    def test_contradicting_decisions_are_an_error(self):
        result = dedup.dedup_postings(self.POSTINGS, review(("JP-0001", "JP-0002", "duplicate"),
                                                            ("JP-0001", "JP-0003", "distinct"),
                                                            ("JP-0002", "JP-0003", "duplicate")))
        self.assertTrue(any("JP-0001 / JP-0003 is 'distinct'" in e for e in result.errors))

    def test_distinct_keeps_both_and_missing_decision_is_unreviewed(self):
        result = dedup.dedup_postings(self.POSTINGS, review(("JP-0001", "JP-0002", "distinct")))
        self.assertEqual(len(result.postings), 4)
        self.assertEqual([(c.posting_ref, c.other_ref) for c in result.unreviewed],
                         [("JP-0001", "JP-0003"), ("JP-0002", "JP-0003")])

    def test_review_of_unknown_or_no_longer_similar_pair(self):
        result = dedup.dedup_postings(self.POSTINGS, review(("JP-0001", "JP-0004", "distinct"),
                                                            ("JP-0001", "JP-0099", "duplicate")))
        self.assertTrue(any("JP-0001 / JP-0004 reviewed but no longer a candidate" in w for w in result.warnings))
        self.assertTrue(any("JP-0099 is not an active posting" in e for e in result.errors))


class ReviewFileTest(RawFileCase):
    def write_review(self, text: str) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "dedup_review.csv"
        path.write_text(text, encoding="utf-8")
        return path

    def test_invalid_rows_are_reported(self):
        path = self.write_review("posting_ref,other_ref,decision,similarity,reason\n"
                                 "JP-0002,JP-0001,duplicate,0.9,wrong order\n"
                                 "JP-0001,JP-0003,maybe,0.9,\n")
        _, errors = dedup.load_review(path)
        text = "\n".join(errors)
        self.assertIn("posting_ref must be the lower ref", text)
        self.assertIn("decision must be one of", text)
        self.assertIn("reason is empty", text)

    def test_committed_review_file_is_valid(self):
        _, errors = dedup.load_review()
        self.assertEqual(errors, [])

    def test_file_level_run_stops_on_an_unreviewed_pair(self):
        raw = self.write([posting("JP-0001", requirements=SHARED), posting("JP-0002", requirements=SHARED),
                          posting("JP-0003", requirements=OTHER)])
        empty = self.write_review("posting_ref,other_ref,decision,similarity,reason\n")
        result = dedup.dedup_file(raw, empty)
        self.assertIn("1 candidate pair(s) not in dedup_review.csv", result.errors[0])
        decided = self.write_review("posting_ref,other_ref,decision,similarity,reason\n"
                                    "JP-0001,JP-0002,duplicate,1.000,same text\n")
        result = dedup.dedup_file(raw, decided)
        self.assertEqual(result.errors, [])
        self.assertEqual([p["posting_ref"] for p in result.postings], ["JP-0001", "JP-0003"])


if __name__ == "__main__":
    unittest.main()
