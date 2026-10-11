"""Clean raw job postings (Phase 3, DATASET_SPEC §17).

Used as a module by the job posting pipeline: clean_file() returns cleaned
postings in memory. Nothing is written to disk, because the cleaned text is
still the posting text and must not be committed (ADR 0012 §2).

Cleaning changes format only, never meaning:
  text columns   newlines kept (\\n), bullets -> "- ", spaces and blank lines collapsed
  short columns  one line, single spaces
  source_url     canonical form without tracking parameters (key for dedup)
  location       English province (jobs/location_map.csv) + work_mode
  employment     one of EMPLOYMENT_TYPES
Removing salary or place names from job titles is NOT done here: that is
Job Title Normalization, after deduplication (IMPLEMENTATION_PLAN §14).

Run from the repository root:  py -3.13 scripts/dataset/clean.py [path/to/file.csv]
It prints counts only, never posting text.
Standard library only (ADR 0010 §6).
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from check_raw import DEFAULT_FILE, check
from common import JOB_CONFIG, rel

LOCATION_MAP = JOB_CONFIG / "location_map.csv"

TEXT_COLUMNS = ["responsibilities", "requirements", "description"]
LINE_COLUMNS = ["job_title", "company", "experience", "education"]

# Characters that are invisible or are a space in disguise
ZERO_WIDTH = re.compile("[​‌‍⁠﻿]")
SPACES = re.compile("[ \t  -  　]+")
# A bullet at the start of a line (Word's private-use bullet is )
BULLET = re.compile("^[•●▪◦·‣⁃■►➢*]\\s*")

# Canonical URL per source: only the job id is kept (ADR 0012 §2 keeps the URL)
URL_PATTERNS = {
    "JobsDB": (re.compile(r"^(?:www\.)?th\.jobsdb\.com$"), re.compile(r"^/(?:th/)?job/(\d+)/?$"),
               "https://th.jobsdb.com/job/{}"),
    "JobThai": (re.compile(r"^(?:www\.)?jobthai\.com$"), re.compile(r"^/(?:th|en)/job/(\d+)/?$"),
                "https://www.jobthai.com/th/job/{}"),
}

# Work mode written next to the place, e.g. "Bangkok (Hybrid)"
WORK_MODE = re.compile(r"\(?\s*\b(hybrid|remote|work from home|wfh|on[\s-]?site)\b\s*\)?", re.IGNORECASE)
WORK_MODES = {"hybrid": "Hybrid", "remote": "Remote", "work from home": "Remote", "wfh": "Remote",
              "onsite": "Onsite", "on-site": "Onsite", "on site": "Onsite"}

EMPLOYMENT_TYPES = {
    "full time": "Full-time", "full-time": "Full-time", "fulltime": "Full-time", "permanent": "Full-time",
    "งานประจำ": "Full-time",
    "contract": "Contract", "contract/temp": "Contract", "temporary": "Contract", "temp": "Contract",
    "สัญญาจ้าง": "Contract",
    "internship": "Internship", "intern": "Internship", "ฝึกงาน": "Internship",
    "part time": "Part-time", "part-time": "Part-time", "พาร์ทไทม์": "Part-time",
}


@dataclass
class CleanResult:
    postings: list[dict[str, str]] = field(default_factory=list)
    excluded: list[tuple[str, str]] = field(default_factory=list)   # (posting_ref, reason)
    changes: Counter = field(default_factory=Counter)               # rule -> postings changed
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------- field rules
def clean_text(text: str) -> str:
    """Multi-line text: keep line breaks, tidy everything else."""
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    text = ZERO_WIDTH.sub("", text)
    lines = [BULLET.sub("- ", SPACES.sub(" ", line).strip()) for line in text.split("\n")]
    out: list[str] = []
    for line in lines:
        if line or (out and out[-1]):   # at most one blank line in a row
            out.append(line)
    return "\n".join(out).strip()


def clean_line(text: str) -> str:
    """Short field: one line, single spaces."""
    text = ZERO_WIDTH.sub("", unicodedata.normalize("NFC", text))
    return re.sub(r"\s+", " ", text).strip()


def canonical_url(url: str, source: str) -> str:
    """https://<site>/job/<id> without query or fragment. ValueError if the shape is unknown."""
    if source not in URL_PATTERNS:
        raise ValueError(f"no URL rule for source '{source}'")
    host, path, template = URL_PATTERNS[source]
    parts = urlsplit(url.strip())
    match = path.match(parts.path) if host.match(parts.netloc.lower()) else None
    if not match:
        raise ValueError(f"source_url does not look like a {source} job page")
    return template.format(match.group(1))


def load_location_map(path: Path = LOCATION_MAP) -> dict[str, str]:
    with path.open(encoding="utf-8", newline="") as f:
        return {clean_line(r["location"]).casefold(): r["province"].strip() for r in csv.DictReader(f)}


def parse_location(text: str, location_map: dict[str, str]) -> tuple[str, str]:
    """'Bangkok (Hybrid)' -> ('Bangkok', 'Hybrid'). Empty stays empty (not stated).
    KeyError if the place is not in jobs/location_map.csv."""
    text = clean_line(text)
    mode = WORK_MODE.search(text)
    work_mode = WORK_MODES[re.sub(r"\s+", " ", mode.group(1).lower())] if mode else ""
    place = WORK_MODE.sub(" ", text).strip(" ,-/")
    place = re.sub(r"\s+", " ", place)
    if not place:
        return "", work_mode
    return location_map[place.casefold()], work_mode


def employment_type(text: str) -> str:
    """Canonical employment type. Empty stays empty. KeyError if unknown."""
    text = clean_line(text)
    return EMPLOYMENT_TYPES[text.lower()] if text else ""


# ---------------------------------------------------------------- pipeline step
def clean_rows(active: list[dict[str, str]], location_map: dict[str, str]) -> CleanResult:
    """Clean the active rows returned by check_raw.check()."""
    result = CleanResult()
    for v in active:
        ref = v["posting_ref"]
        p = dict(v)
        for column in TEXT_COLUMNS:
            p[column] = clean_text(v[column])
        for column in LINE_COLUMNS:
            p[column] = clean_line(v[column])
        p["search_keyword"] = clean_line(v["search_keyword"]).lower()
        p["notes"] = clean_line(v["notes"])

        try:
            p["source_url"] = canonical_url(v["source_url"], v["source"])
        except ValueError as e:
            result.errors.append(f"{ref:<9} {e}")
        try:
            p["location"], p["work_mode"] = parse_location(v["location"], location_map)
        except KeyError:
            p["work_mode"] = ""
            result.errors.append(f"{ref:<9} location '{clean_line(v['location'])}' is not in "
                                 f"jobs/location_map.csv: add a row with its English province")
        try:
            p["employment_type"] = employment_type(v["employment_type"])
        except KeyError:
            result.errors.append(f"{ref:<9} employment_type '{clean_line(v['employment_type'])}' is unknown: "
                                 f"add it to EMPLOYMENT_TYPES in clean.py")

        for column in TEXT_COLUMNS + LINE_COLUMNS + ["source_url", "location", "employment_type"]:
            if p[column] != v[column]:
                result.changes[column] += 1
        result.postings.append(p)
    return result


def clean_file(path: Path = DEFAULT_FILE) -> CleanResult:
    """check_raw.check() then clean_rows(). Errors from either step are in .errors."""
    raw = check(path)
    if raw.errors:
        return CleanResult(errors=["raw file has errors: run check_raw.py first"] + raw.errors,
                           warnings=raw.warnings)
    result = clean_rows(raw.active, load_location_map())
    result.excluded = [(v["posting_ref"], v["notes"][len("exclude:"):].strip()) for v in raw.excluded]
    result.warnings = raw.warnings + result.warnings
    return result


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FILE
    if not path.is_file():
        print(f"ERROR: {path} not found (see COLLECTION_GUIDE.md §1)")
        sys.exit(1)
    result = clean_file(path)
    if result.errors:
        print(f"{len(result.errors)} ERROR(S)")
        print("\n".join(result.errors))
        sys.exit(1)

    print(f"File: {rel(path) if path.is_relative_to(DEFAULT_FILE.parents[4]) else path}")
    print(f"Cleaned postings: {len(result.postings)}  excluded: {len(result.excluded)}")
    print("Postings changed per column:")
    for column, n in sorted(result.changes.items()):
        print(f"  {column:<16} {n}")
    print("Province:       ", dict(Counter(p["location"] or "(not stated)" for p in result.postings).most_common()))
    print("Work mode:      ", dict(Counter(p["work_mode"] or "(not stated)" for p in result.postings).most_common()))
    print("Employment type:", dict(Counter(p["employment_type"] or "(not stated)" for p in result.postings).most_common()))
    if result.warnings:
        print(f"\n{len(result.warnings)} WARNING(S)")
        print("\n".join(result.warnings))
    print("\nCLEAN OK")


if __name__ == "__main__":
    main()
