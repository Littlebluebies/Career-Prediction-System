"""Validate the processed reference dataset before it is imported.

Checks the files written by build_esco_reference.py against
DATASET_SPEC.md §32-35 (metadata, completeness, consistency, validity,
uniqueness, traceability) and the table rules of DATABASE.md
(unique names, unique aliases, valid categories, foreign keys).

Run from the repository root:  py -3.13 scripts/dataset/validate.py
Exit code 0 = all checks passed, 1 = at least one check failed.
import.py runs the same checks before it writes any seed file.
Standard library only (ADR 0010 §6).
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter

from common import (CAREER_FAMILIES, DATASET_VERSION, FILES, METADATA_DATASETS,
                    RELATION_TYPES, SOURCE_LABEL, VALID_CATEGORIES, metadata_path,
                    read_csv, rel)

ESCO_OCCUPATION_URI = "http://data.europa.eu/esco/occupation/"
ESCO_SKILL_URI = "http://data.europa.eu/esco/skill/"
METADATA_REQUIRED = ["dataset_name", "version", "source", "collection_date", "coverage",
                     "description", "number_of_records", "processing_method"]  # ADR 0006 §3

# columns that must never be empty (DATASET_SPEC §33 Completeness)
REQUIRED_COLUMNS = {
    "occupation": ["career_family_code", "occupation_name", "source", "source_identifier"],
    "occupation_alias": ["occupation_name", "alias"],
    "skill": ["skill_name", "category", "category_rule", "source_identifier"],
    "skill_alias": ["skill_name", "alias"],
    "occupation_skill": ["occupation_name", "skill_name", "relation_type", "source"],
}


class Report:
    def __init__(self) -> None:
        self.failed = 0

    def check(self, ok: bool, label: str, detail: object = "") -> None:
        if ok:
            print(f"PASS  {label}")
        else:
            self.failed += 1
            print(f"FAIL  {label}" + (f"  -> {detail}" if detail != "" else ""))


def duplicates(values) -> list:
    return sorted(v for v, n in Counter(values).items() if n > 1)


def load() -> dict[str, list[dict[str, str]]]:
    missing = [rel(p) for p in FILES.values() if not p.is_file()]
    missing += [rel(metadata_path(n)) for n in METADATA_DATASETS if not metadata_path(n).is_file()]
    if missing:
        print(f"FAIL  processed files exist  -> missing {missing}")
        print("Run scripts/dataset/build_esco_reference.py first.")
        sys.exit(1)
    return {name: read_csv(path) for name, path in FILES.items()}


def run_checks(data: dict[str, list[dict[str, str]]]) -> int:
    """Run every check, print PASS/FAIL lines, return the number of failures."""
    r = Report()
    occ, occ_alias = data["occupation"], data["occupation_alias"]
    skill, skill_alias = data["skill"], data["skill_alias"]
    rel_rows, candidates = data["occupation_skill"], data["candidates"]

    occ_names = {o["occupation_name"] for o in occ}
    skill_names = {s["skill_name"] for s in skill}
    cf_codes = {code for code, _ in CAREER_FAMILIES}

    # ---------------- Completeness (§33)
    for name, cols in REQUIRED_COLUMNS.items():
        empty = [(i + 2, c) for i, row in enumerate(data[name]) for c in cols if not row.get(c)]
        r.check(not empty, f"completeness: {name} required columns filled", empty[:5])
    r.check(len(occ) > 0 and len(skill) > 0 and len(rel_rows) > 0,
            "completeness: occupation, skill and occupation_skill are not empty")

    # ---------------- Consistency (§33)
    padded = [(name, row[c]) for name in REQUIRED_COLUMNS for row in data[name]
              for c in REQUIRED_COLUMNS[name] if row[c] != row[c].strip()]
    r.check(not padded, "consistency: no leading/trailing spaces in key columns", padded[:5])
    r.check(all(o["source"] == SOURCE_LABEL for o in occ),
            f"consistency: occupation.source = '{SOURCE_LABEL}'")
    r.check(all(x["source"] == f"{SOURCE_LABEL}: {x['relation_type']}" for x in rel_rows),
            "consistency: occupation_skill.source = '<source>: <relation_type>'")

    # ---------------- Validity (§33, §34, §35)
    bad_cf = sorted({o["career_family_code"] for o in occ} - cf_codes)
    r.check(not bad_cf, "validity: career_family_code exists in DATABASE.md §19", bad_cf)
    bad_cat = sorted({s["category"] for s in skill} - VALID_CATEGORIES)
    r.check(not bad_cat, "validity: skill.category allowed by chk_skill_category", bad_cat)
    bad_type = sorted({x["relation_type"] for x in rel_rows} - RELATION_TYPES)
    r.check(not bad_type, "validity: relation_type is essential or optional", bad_type)
    bad_rule = [s["skill_name"] for s in skill
                if not re.match(r"^(R[1-6] \S+|OVERRIDE: .+)$", s["category_rule"])]
    r.check(not bad_rule, "validity: every category has a recorded rule or override reason (§34)",
            bad_rule[:5])

    # ---------------- Uniqueness (§33, §35, DATABASE.md UNIQUE constraints)
    r.check(not duplicates(o["occupation_name"].lower() for o in occ),
            "uniqueness: occupation_name", duplicates(o["occupation_name"].lower() for o in occ))
    r.check(not duplicates(o["source_identifier"] for o in occ), "uniqueness: occupation source_identifier")
    r.check(not duplicates(s["skill_name"].lower() for s in skill),
            "uniqueness: skill_name (case-insensitive)", duplicates(s["skill_name"].lower() for s in skill))
    r.check(not duplicates(s["source_identifier"] for s in skill), "uniqueness: skill source_identifier")
    r.check(not duplicates(a["alias"].lower() for a in skill_alias),
            "uniqueness: skill_alias.alias", duplicates(a["alias"].lower() for a in skill_alias)[:5])
    r.check(not duplicates(a["alias"].lower() for a in occ_alias),
            "uniqueness: occupation_alias.alias", duplicates(a["alias"].lower() for a in occ_alias)[:5])
    r.check(not duplicates((x["occupation_name"], x["skill_name"]) for x in rel_rows),
            "uniqueness: one relation per occupation-skill pair")

    # ---------------- Alias rules (§9.1, §34, §35 "Alias ไม่ขัดแย้ง")
    lower_skills = {n.lower() for n in skill_names}
    clash = [a["alias"] for a in skill_alias if a["alias"].lower() in lower_skills]
    r.check(not clash, "alias: no skill alias equals a canonical skill name", clash[:5])
    lower_occs = {n.lower() for n in occ_names}
    clash = [a["alias"] for a in occ_alias if a["alias"].lower() in lower_occs]
    r.check(not clash, "alias: no occupation alias equals an occupation name", clash[:5])

    # ---------------- Referential integrity between files (= foreign keys)
    orphan = sorted({a["skill_name"] for a in skill_alias} - skill_names)
    r.check(not orphan, "reference: skill_alias.skill_name exists in skill.csv", orphan[:5])
    orphan = sorted({a["occupation_name"] for a in occ_alias} - occ_names)
    r.check(not orphan, "reference: occupation_alias.occupation_name exists in occupation.csv", orphan[:5])
    orphan = sorted({x["occupation_name"] for x in rel_rows} - occ_names)
    r.check(not orphan, "reference: occupation_skill.occupation_name exists", orphan[:5])
    orphan = sorted({x["skill_name"] for x in rel_rows} - skill_names)
    r.check(not orphan, "reference: occupation_skill.skill_name exists", orphan[:5])
    unused = sorted(skill_names - {x["skill_name"] for x in rel_rows})
    r.check(not unused, "reference: every skill is related to at least one occupation", unused[:5])
    no_essential = sorted(occ_names - {x["occupation_name"] for x in rel_rows
                                       if x["relation_type"] == "essential"})
    r.check(not no_essential, "reference: every occupation has at least one essential skill", no_essential)

    # ---------------- Traceability (§33, §35)
    r.check(all(o["source_identifier"].startswith(ESCO_OCCUPATION_URI) for o in occ),
            "traceability: every occupation has an ESCO occupation URI")
    r.check(all(s["source_identifier"].startswith(ESCO_SKILL_URI) for s in skill),
            "traceability: every skill has an ESCO skill URI")
    included = {c["esco_uri"] for c in candidates if c["decision"] == "include"}
    r.check(included == {o["source_identifier"] for o in occ},
            "traceability: occupation.csv = candidates marked 'include' in the review")
    r.check(all(c["decision"] in ("include", "exclude") and c["reason"] for c in candidates),
            "traceability: every candidate has a review decision and reason")

    # ---------------- Metadata (§32, ADR 0006)
    counts = {"occupation": len(occ), "skill": len(skill), "occupation_skill": len(rel_rows)}
    for name in METADATA_DATASETS:
        path = metadata_path(name)
        meta = json.loads(path.read_text(encoding="utf-8"))
        missing = [k for k in METADATA_REQUIRED if meta.get(k) in (None, "")]
        r.check(not missing, f"metadata: {path.name} has every required field", missing)
        r.check(meta.get("dataset_name") == name and meta.get("version") == DATASET_VERSION,
                f"metadata: {path.name} name/version match the file name")
        r.check(bool(re.fullmatch(r"\d{4}\.\d{2}", str(meta.get("version")))),
                f"metadata: {path.name} version format YYYY.NN (ADR 0010 §4)")
        r.check(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(meta.get("collection_date")))),
                f"metadata: {path.name} collection_date is YYYY-MM-DD")
        r.check(meta.get("number_of_records") == counts[name],
                f"metadata: {path.name} number_of_records = rows in the processed file",
                f"{meta.get('number_of_records')} != {counts[name]}")
        r.check(bool(meta.get("source_files")),
                f"metadata: {path.name} records SHA-256 of the raw files (ADR 0010 §5)")

    return r.failed


def main() -> None:
    print(f"Validating reference dataset {DATASET_VERSION}")
    failed = run_checks(load())
    if failed:
        print(f"\n{failed} CHECK(S) FAILED")
        sys.exit(1)
    print("\nALL DATASET CHECKS PASSED")


if __name__ == "__main__":
    main()
