"""Check the raw job posting file collected by hand (Phase 3).

Reads  datasets/raw/job_posting/<version>/job_postings.csv  (not in Git, ADR 0012 §2)
and reports problems per posting_ref. It never prints the posting text,
only references, column names and short matched fragments, so the output
is safe to paste into a chat or a CI log.

Rules: scripts/dataset/jobs/COLLECTION_GUIDE.md, ADR 0012, DATASET_SPEC §12-18

Run from the repository root:  py -3.13 scripts/dataset/check_raw.py [path/to/file.csv]
Exit code 0 = no errors (warnings allowed), 1 = at least one error.
Standard library only (ADR 0010 §6).
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from common import JOB_CONFIG, JOB_RAW, rel

TEMPLATE = JOB_CONFIG / "job_posting_template.csv"
DEFAULT_FILE = JOB_RAW / "job_postings.csv"

SOURCES = {"JobsDB", "JobThai"}
SEARCH_KEYWORDS = {  # COLLECTION_GUIDE.md §2
    "frontend developer", "front-end developer", "ui developer",
    "backend developer", "back-end developer",
    "full stack developer", "fullstack developer",
    "web developer", "web application developer", "web programmer",
    "ux ui designer", "ui designer", "ux designer", "web designer",
}
REQUIRED = ["posting_ref", "source", "source_url", "search_keyword", "date_collected", "job_title", "company"]
TEXT_COLUMNS = ["responsibilities", "requirements", "description", "company", "job_title", "notes"]
SHORT_COLUMNS = {"job_title": 120, "company": 120, "location": 80, "employment_type": 40}

# Personal data that must never be collected (COLLECTION_GUIDE.md §5)
PII_PATTERNS = {
    "email address": re.compile(r"[\w.+-]+@[\w-]+\.[A-Za-z]{2,}"),
    "phone number": re.compile(r"(?<!\d)(?:\+66|0)[\s-]?\d{1,2}[\s-]?\d{3}[\s-]?\d{3,4}(?!\d)"),
    "LINE ID": re.compile(r"(?i)\bline\s*(?:id)?\s*[:@]"),
}

# Rough occupation tally from job titles, for collection progress only.
# The real mapping is done (and reviewed) later in the pipeline.
ROUGH_OCCUPATION = [
    ("Full-stack", re.compile(r"(?i)full[\s-]?stack")),
    ("Back-end", re.compile(r"(?i)back[\s-]?end")),
    ("Front-end", re.compile(r"(?i)front[\s-]?end|\bui developer")),
    ("UI/UX Designer", re.compile(r"(?i)\bux\b|\bui\b.*designer|user experience")),
    ("Web Designer", re.compile(r"(?i)web designer")),
    ("Web Developer", re.compile(r"(?i)web|programmer")),
]


def parse_date(text: str) -> date | None:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def url_key(url: str) -> str:
    """URL without query string / fragment: tracking parameters differ between visits."""
    return url.split("?")[0].split("#")[0].rstrip("/").lower()


def rough_occupation(title: str) -> str:
    for name, pattern in ROUGH_OCCUPATION:
        if pattern.search(title):
            return name
    return "unclassified"


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FILE
    if not path.is_file():
        print(f"ERROR: {path} not found (see COLLECTION_GUIDE.md §1)")
        sys.exit(1)

    errors: list[str] = []
    warnings: list[str] = []

    with TEMPLATE.open(encoding="utf-8", newline="") as f:
        expected = next(csv.reader(f))
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)
    if header != expected:
        print("ERROR: columns differ from job_posting_template.csv")
        print("  missing:", [c for c in expected if c not in header])
        print("  extra:  ", [c for c in header if c not in expected])
        sys.exit(1)

    def err(ref: str, msg: str) -> None:
        errors.append(f"{ref:<9} {msg}")

    def warn(ref: str, msg: str) -> None:
        warnings.append(f"{ref:<9} {msg}")

    value = {id(r): {k: (v or "").strip() for k, v in r.items()} for r in rows}

    # posting_ref: format and uniqueness (also for unfilled / excluded rows)
    refs = Counter(value[id(r)]["posting_ref"] for r in rows)
    for ref, n in refs.items():
        if not re.fullmatch(r"JP-\d{4}", ref):
            err(ref or "(empty)", "posting_ref is not JP-0000 format")
        if n > 1:
            err(ref, f"posting_ref used {n} times")

    unfilled, excluded, active = [], [], []
    for r in rows:
        v = value[id(r)]
        if not v["job_title"] and not v["source_url"]:
            unfilled.append(v["posting_ref"])
        elif v["notes"].lower().startswith("exclude:"):
            excluded.append(v)
        else:
            active.append(v)

    for v in excluded:
        if len(v["notes"]) <= len("exclude:"):
            err(v["posting_ref"], "excluded without a reason after 'exclude:'")
        target = re.search(r"merged into (JP-\d{4})", v["notes"])
        if target and target.group(1) not in refs:
            err(v["posting_ref"], f"merged into {target.group(1)}, which does not exist")

    seen_url_title: dict[tuple[str, str], str] = {}
    by_url: dict[str, list[dict]] = defaultdict(list)
    for v in active:
        ref = v["posting_ref"]
        missing = [c for c in REQUIRED if not v[c]]
        if not (v["requirements"] or v["description"]):
            missing.append("requirements or description")
        if missing:
            err(ref, "missing: " + ", ".join(missing))
        if v["source"] and v["source"] not in SOURCES:
            err(ref, f"source '{v['source']}' is not one of {sorted(SOURCES)}")
        if v["search_keyword"] and v["search_keyword"].lower() not in SEARCH_KEYWORDS:
            warn(ref, f"search_keyword '{v['search_keyword']}' is not in the guide's list")
        if v["source_url"] and not v["source_url"].lower().startswith(("http://", "https://")):
            err(ref, "source_url is not a URL (columns swapped?)")

        collected = parse_date(v["date_collected"]) if v["date_collected"] else None
        if v["date_collected"] and collected is None:
            err(ref, f"date_collected '{v['date_collected']}' is not a valid YYYY-MM-DD date")
        if v["date_posted"]:
            posted = parse_date(v["date_posted"])
            if posted is None:
                err(ref, f"date_posted '{v['date_posted']}' is not a valid YYYY-MM-DD date")
            elif collected and posted > collected:
                err(ref, "date_posted is after date_collected")

        for column, limit in SHORT_COLUMNS.items():
            if len(v[column]) > limit:
                err(ref, f"{column} is {len(v[column])} characters (text pasted into the wrong column?)")
        for column in TEXT_COLUMNS:
            for label, pattern in PII_PATTERNS.items():
                match = pattern.search(v[column])
                if match:
                    err(ref, f"possible {label} in {column}: replace it with [removed]")

        key = (url_key(v["source_url"]), v["job_title"].lower())
        if key in seen_url_title:
            err(ref, f"duplicate of {seen_url_title[key]} (same URL and job title)")
        else:
            seen_url_title[key] = ref
        by_url[url_key(v["source_url"])].append(v)

    # Same URL in several active rows is fine only for documented splits
    for url, group in by_url.items():
        if len(group) > 1:
            for v in group:
                if "split from multi-role" not in v["notes"].lower():
                    warn(v["posting_ref"], "same URL as " + ", ".join(
                        g["posting_ref"] for g in group if g is not v) + " without a 'split from multi-role' note")
    # Same company + same rough occupation + same URL looks like a level split (ADR 0012 §9)
    for url, group in by_url.items():
        occupations = Counter(rough_occupation(v["job_title"]) for v in group)
        for occ, n in occupations.items():
            if n > 1:
                warn(", ".join(v["posting_ref"] for v in group if rough_occupation(v["job_title"]) == occ),
                     f"one posting, {n} rows of the same occupation ({occ}): merge levels into one row (ADR 0012 §9)")

    # ---------------- report
    print(f"File: {rel(path) if path.is_relative_to(JOB_RAW.parents[3]) else path}")
    print(f"Rows: {len(rows)}  active: {len(active)}  excluded: {len(excluded)}  not filled yet: {len(unfilled)}")
    dates = sorted(v["date_collected"] for v in active if parse_date(v["date_collected"]))
    if dates:
        print(f"Collection period so far: {dates[0]} .. {dates[-1]}")
    print("By source:  ", dict(Counter(v["source"] for v in active)))
    print("By keyword: ", dict(Counter(v["search_keyword"] for v in active)))
    print("Rough occupation count (from titles, progress only):")
    for occ, n in Counter(rough_occupation(v["job_title"]) for v in active).most_common():
        print(f"  {occ:<16} {n}")
    if excluded:
        print("Excluded:")
        for v in excluded:
            print(f"  {v['posting_ref']}  {v['notes'][:80]}")

    if warnings:
        print(f"\n{len(warnings)} WARNING(S)")
        print("\n".join(warnings))
    if errors:
        print(f"\n{len(errors)} ERROR(S)")
        print("\n".join(errors))
        sys.exit(1)
    print("\nRAW FILE OK" + (" (with warnings)" if warnings else ""))


if __name__ == "__main__":
    main()
