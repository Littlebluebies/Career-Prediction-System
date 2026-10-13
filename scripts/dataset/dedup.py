"""Find duplicate job postings and apply the researcher's decisions (Phase 3).

DATASET_SPEC §18, ADR 0012 §12. Runs on the output of clean.py, in memory.

1. Candidate pairs (research parameters, recorded in metadata):
   - similarity of requirements + responsibilities >= SIMILARITY_THRESHOLD, or
   - one long text column identical in both postings.
   Rows that share one canonical URL are documented splits (ADR 0012 §9,
   checked by check_raw.py) and are never candidates.
2. Every candidate pair must have a decision in jobs/dedup_review.csv
   (duplicate | distinct). An unreviewed pair stops the pipeline.
3. For each group of duplicates the lowest posting_ref is kept.

Run from the repository root:  py -3.13 scripts/dataset/dedup.py [path/to/file.csv]
It prints posting_refs, sources and scores only, never posting text.
Standard library only (ADR 0010 §6).
"""

from __future__ import annotations

import csv
import difflib
import itertools
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from check_raw import DEFAULT_FILE
from clean import TEXT_COLUMNS, clean_file
from common import JOB_CONFIG, rel

REVIEW = JOB_CONFIG / "dedup_review.csv"
REVIEW_COLUMNS = ["posting_ref", "other_ref", "decision", "similarity", "reason"]
DECISIONS = {"duplicate", "distinct"}

SIMILARITY_THRESHOLD = 0.60   # difflib ratio of requirements + responsibilities
PREFILTER_JACCARD = 0.25      # word-set overlap below this is not compared (speed only)
IDENTICAL_MIN_CHARS = 80      # shorter identical text is too generic to mean anything


@dataclass
class Candidate:
    posting_ref: str      # lower ref
    other_ref: str
    similarity: float
    identical: list[str]  # text columns that are exactly the same
    sources: tuple[str, str] = ("", "")


@dataclass
class DedupResult:
    postings: list[dict[str, str]] = field(default_factory=list)       # kept postings
    duplicates: list[tuple[str, str, str]] = field(default_factory=list)  # (ref, duplicate_of, reason)
    candidates: list[Candidate] = field(default_factory=list)
    unreviewed: list[Candidate] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------- candidates
def compared_text(p: dict[str, str]) -> str:
    return p["requirements"] + "\n" + p["responsibilities"]


def words(text: str) -> set[str]:
    return set(re.findall(r"\w+", text.lower()))


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def find_candidates(postings: list[dict[str, str]]) -> list[Candidate]:
    text = {p["posting_ref"]: compared_text(p) for p in postings}
    word_sets = {ref: words(t) for ref, t in text.items()}
    found = []
    for a, b in itertools.combinations(sorted(postings, key=lambda p: p["posting_ref"]), 2):
        if a["source_url"] == b["source_url"]:
            continue   # documented split of one posting
        ra, rb = a["posting_ref"], b["posting_ref"]
        identical = [c for c in TEXT_COLUMNS if len(a[c]) > IDENTICAL_MIN_CHARS and a[c] == b[c]]
        union = word_sets[ra] | word_sets[rb]
        overlap = len(word_sets[ra] & word_sets[rb]) / len(union) if union else 0.0
        score = similarity(text[ra], text[rb]) if overlap >= PREFILTER_JACCARD or identical else 0.0
        if score >= SIMILARITY_THRESHOLD or identical:
            found.append(Candidate(ra, rb, round(score, 3), identical, (a["source"], b["source"])))
    return found


# ---------------------------------------------------------------- review file
def load_review(path: Path = REVIEW) -> tuple[dict[tuple[str, str], dict[str, str]], list[str]]:
    """(pair -> row, errors). Pairs are (lower ref, higher ref)."""
    errors: list[str] = []
    review: dict[tuple[str, str], dict[str, str]] = {}
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != REVIEW_COLUMNS:
            return {}, [f"{path.name}: columns must be {REVIEW_COLUMNS}"]
        for line, row in enumerate(reader, start=2):
            row = {k: (v or "").strip() for k, v in row.items()}
            pair = (row["posting_ref"], row["other_ref"])
            where = f"{path.name} line {line}"
            if not pair[0] < pair[1]:
                errors.append(f"{where}: posting_ref must be the lower ref of the pair")
            if row["decision"] not in DECISIONS:
                errors.append(f"{where}: decision must be one of {sorted(DECISIONS)}")
            if not row["reason"]:
                errors.append(f"{where}: reason is empty")
            if pair in review:
                errors.append(f"{where}: pair {pair[0]} / {pair[1]} is listed twice")
            review[pair] = row
    return review, errors


# ---------------------------------------------------------------- pipeline step
def dedup_postings(postings: list[dict[str, str]],
                   review: dict[tuple[str, str], dict[str, str]]) -> DedupResult:
    result = DedupResult(candidates=find_candidates(postings))
    refs = {p["posting_ref"] for p in postings}
    candidate_pairs = {(c.posting_ref, c.other_ref) for c in result.candidates}

    for (a, b), row in review.items():
        if a not in refs or b not in refs:
            result.errors.append(f"dedup_review.csv: {a} / {b} is not an active posting (excluded or renamed?)")
        elif (a, b) not in candidate_pairs:
            result.warnings.append(f"{a} / {b} reviewed but no longer a candidate (text changed?): "
                                   f"check the row in dedup_review.csv")
    result.unreviewed = [c for c in result.candidates if (c.posting_ref, c.other_ref) not in review]

    # Groups of duplicates (A=B and B=C means one posting); keep the lowest ref
    parent = {ref: ref for ref in refs}

    def root(ref: str) -> str:
        while parent[ref] != ref:
            ref = parent[ref]
        return ref

    reasons: dict[str, str] = {}
    for (a, b), row in sorted(review.items()):
        if row["decision"] == "duplicate" and a in refs and b in refs:
            ra, rb = root(a), root(b)
            parent[max(ra, rb)] = min(ra, rb)
            reasons.setdefault(b, row["reason"])
            reasons.setdefault(a, row["reason"])
    # A=B and B=C makes A=C, so "A / C distinct" would contradict the other decisions
    for (a, b), row in sorted(review.items()):
        if row["decision"] == "distinct" and a in refs and b in refs and root(a) == root(b):
            result.errors.append(f"dedup_review.csv: {a} / {b} is 'distinct' but other 'duplicate' "
                                 f"decisions put both in one group: fix the decisions")
    for p in sorted(postings, key=lambda p: p["posting_ref"]):
        ref = p["posting_ref"]
        if root(ref) == ref:
            result.postings.append(p)
        else:
            result.duplicates.append((ref, root(ref), reasons[ref]))
    return result


def dedup_file(path: Path = DEFAULT_FILE, review_path: Path = REVIEW) -> DedupResult:
    """clean_file() then dedup_postings(). Errors from any step are in .errors."""
    cleaned = clean_file(path)
    if cleaned.errors:
        return DedupResult(errors=["cleaning failed: run clean.py first"] + cleaned.errors,
                           warnings=cleaned.warnings)
    review, errors = load_review(review_path)
    if errors:
        return DedupResult(errors=errors, warnings=cleaned.warnings)
    result = dedup_postings(cleaned.postings, review)
    if result.unreviewed:
        result.errors.append(f"{len(result.unreviewed)} candidate pair(s) not in dedup_review.csv: "
                             "add a decision for each (lines below)")
    result.warnings = cleaned.warnings + result.warnings
    return result


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FILE
    if not path.is_file():
        print(f"ERROR: {path} not found (see COLLECTION_GUIDE.md §1)")
        sys.exit(1)
    result = dedup_file(path)

    print(f"Review file: {rel(REVIEW)}")
    print(f"Parameters: similarity >= {SIMILARITY_THRESHOLD}, prefilter Jaccard >= {PREFILTER_JACCARD}, "
          f"identical text > {IDENTICAL_MIN_CHARS} characters")
    print(f"Candidate pairs: {len(result.candidates)}  unreviewed: {len(result.unreviewed)}")
    for c in result.candidates:
        same = f"  identical: {', '.join(c.identical)}" if c.identical else ""
        print(f"  {c.posting_ref} ({c.sources[0]}) / {c.other_ref} ({c.sources[1]})  "
              f"similarity {c.similarity:.3f}{same}")
    if result.duplicates:
        print("Removed as duplicates:")
        for ref, of, reason in result.duplicates:
            print(f"  {ref} -> duplicate of {of}: {reason}")
    if result.warnings:
        print(f"\n{len(result.warnings)} WARNING(S)")
        print("\n".join(result.warnings))
    if result.errors:
        print(f"\n{len(result.errors)} ERROR(S)")
        print("\n".join(result.errors))
        for c in result.unreviewed:
            print(f"{c.posting_ref},{c.other_ref},,{c.similarity:.3f},")
        sys.exit(1)
    print(f"\nPostings after dedup: {len(result.postings)}")
    print("DEDUP OK")


if __name__ == "__main__":
    main()
