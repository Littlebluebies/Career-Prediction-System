"""Build the Phase 2 reference dataset (Semester 1 pilot) from ESCO.

Raw ESCO CSV (datasets/raw/esco/<version>/, not in Git)
    -> candidate occupations (keyword search, reproducible)
    -> researcher-reviewed selection   (scripts/dataset/esco/occupation_selection.csv)
    -> occupations, skills, aliases, occupation-skill relations
    -> skill categories (hierarchy rules + reviewed overrides)
    -> datasets/processed/...  +  datasets/metadata/*.json

Decisions: docs/decisions/0010-phase-2-reference-data-decisions.md
Rules:     DATASET_SPEC.md §2, §5, §7-9, §31-35, §58
Run from the repository root:  py -3.13 scripts/dataset/build_esco_reference.py
Standard library only (ADR 0010 §6).
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

from common import (CONFIG, DATASET_VERSION, DOWNLOAD_DATE, FILES, METADATA, RAW,
                    SOURCE_LABEL, VALID_CATEGORIES, fail, metadata_path, read_csv, rel)

PROCESSING_VERSION = "build_esco_reference.py 1"

RAW_FILES = [
    "occupations_en.csv",
    "skills_en.csv",
    "occupationSkillRelations_en.csv",
    "broaderRelationsSkillPillar_en.csv",
    "skillGroups_en.csv",
]

# Target occupations of the Semester 1 pilot (DATASET_SPEC §38) and the
# patterns used to search ESCO preferred + alternative labels.
TARGETS = {
    "Front-end Developer": r"front[\s-]?end",
    "Back-end Developer": r"back[\s-]?end",
    "Full-stack Developer": r"full[\s-]?stack",
    "Web Developer": r"\bweb developer",
    "Web Application Developer": r"\bweb application developer",
    "UI/UX Designer": r"\bui\b|\bux\b|user interface|user experience",
}

# Skill category rules (ADR 0010 addendum, Phase 2 decision A).
# Checked in order; the first rule whose ESCO group code is an ancestor wins.
CATEGORY_RULES = [
    ("R1", ("S1.11", "S1.12"), "DESIGN"),
    ("R2", ("S1",), "COMMUNICATION"),
    ("R3", ("S4", "04"), "BUSINESS"),
    ("R4", ("02",), "CREATIVE"),
    ("R5", ("06", "S5", "S7"), "TECHNICAL"),
    ("R6", ("S2", "03"), "OTHER"),
]


# ---------------------------------------------------------------- helpers
def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {rel(path)} ({len(rows)} rows)")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def labels(text: str) -> list[str]:
    """ESCO stores alternative labels one per line inside one cell."""
    return [x.strip() for x in text.split("\n") if x.strip()]


def group_matches(code: str, prefix: str) -> bool:
    # "S1" matches S1, S1.2 ...; "06" matches 06, 061, 0613 ...
    if prefix[0].isalpha():
        return code == prefix or code.startswith(prefix + ".")
    return code.startswith(prefix)


# ---------------------------------------------------------------- steps
def load_raw():
    if not RAW.is_dir():
        fail(f"{rel(RAW)} not found. Download ESCO {ESCO_VERSION} first (ADR 0010).")
    for name in RAW_FILES:
        if not (RAW / name).is_file():
            fail(f"missing raw file {name}")
    return {name: read_csv(RAW / name) for name in RAW_FILES}


def find_candidates(occupations):
    """Reproducible keyword search over preferred + alternative labels."""
    found = {}
    for o in occupations:
        for target, pattern in TARGETS.items():
            for label in [o["preferredLabel"], *labels(o["altLabels"])]:
                if re.search(pattern, label, re.IGNORECASE):
                    key = (o["conceptUri"], target)
                    found.setdefault(key, {"target": target, "esco_uri": o["conceptUri"],
                                           "preferred_label": o["preferredLabel"],
                                           "matched_label": label, "isco_code": o["code"]})
                    break
    return list(found.values())


def apply_selection(candidates, occupations_by_uri):
    selection = {r["esco_uri"]: r for r in read_csv(CONFIG / "occupation_selection.csv")}
    candidate_uris = {c["esco_uri"] for c in candidates}

    unreviewed = sorted(candidate_uris - selection.keys())
    if unreviewed:
        names = [occupations_by_uri[u]["preferredLabel"] for u in unreviewed]
        fail(f"candidates without a review decision in occupation_selection.csv: {names}")
    for uri, row in selection.items():
        if uri not in occupations_by_uri:
            fail(f"selection refers to unknown ESCO occupation {uri}")
        if row["decision"] not in ("include", "exclude"):
            fail(f"invalid decision for {row['preferred_label']}: {row['decision']}")
        if row["decision"] == "include" and not row["career_family_code"]:
            fail(f"included occupation {row['preferred_label']} needs a career_family_code")
        if not row["reason"]:
            fail(f"decision for {row['preferred_label']} has no reason")

    for c in candidates:
        s = selection[c["esco_uri"]]
        c.update(decision=s["decision"], career_family_code=s["career_family_code"], reason=s["reason"])
    included = [selection[u] for u in selection if selection[u]["decision"] == "include"]
    return included


def build_occupations(included, occupations_by_uri):
    occ_rows, alias_rows = [], []
    owner = defaultdict(set)
    for s in included:
        o = occupations_by_uri[s["esco_uri"]]
        occ_rows.append({"career_family_code": s["career_family_code"],
                         "occupation_name": o["preferredLabel"],
                         "description": o["description"],
                         "source": SOURCE_LABEL,
                         "source_identifier": o["conceptUri"],
                         "isco_code": o["code"]})
        for a in labels(o["altLabels"]):
            owner[a.lower()].add((o["preferredLabel"], a))
    names = {r["occupation_name"].lower() for r in occ_rows}
    dropped = []
    for key, owners in owner.items():
        occ_names = {n for n, _ in owners}
        if len(occ_names) > 1 or key in names:
            dropped.append({"entity": "occupation", "alias": key,
                            "reason": "ambiguous or equals an occupation name",
                            "owners": "; ".join(sorted(occ_names))})
            continue
        name, original = sorted(owners)[0]
        alias_rows.append({"occupation_name": name, "alias": original})
    return (sorted(occ_rows, key=lambda r: r["occupation_name"]),
            sorted(alias_rows, key=lambda r: (r["occupation_name"], r["alias"].lower())),
            dropped)


def build_skills(raw, included_uris):
    skills_by_uri = {s["conceptUri"]: s for s in raw["skills_en.csv"]}
    relations = [r for r in raw["occupationSkillRelations_en.csv"] if r["occupationUri"] in included_uris]
    skill_uris = {r["skillUri"] for r in relations}
    missing = [u for u in skill_uris if u not in skills_by_uri]
    if missing:
        fail(f"{len(missing)} related skills not found in skills_en.csv")

    # ancestor group codes for each skill (ESCO skill pillar hierarchy)
    broader = defaultdict(list)
    for r in raw["broaderRelationsSkillPillar_en.csv"]:
        broader[r["conceptUri"]].append(r["broaderUri"])
    group_code = {g["conceptUri"]: g.get("code", "") for g in raw["skillGroups_en.csv"]}

    def ancestor_codes(uri):
        seen, stack = set(), [uri]
        while stack:
            for b in broader.get(stack.pop(), []):
                if b not in seen:
                    seen.add(b)
                    stack.append(b)
        return {group_code[a] for a in seen if group_code.get(a)}

    overrides = {r["skill_name"]: r for r in read_csv(CONFIG / "category_overrides.csv")}
    pilot_names = {skills_by_uri[u]["preferredLabel"] for u in skill_uris}
    unknown = sorted(set(overrides) - pilot_names)
    if unknown:
        fail(f"category_overrides.csv lists skills outside the pilot set: {unknown}")

    skill_rows = []
    for uri in skill_uris:
        s = skills_by_uri[uri]
        name = s["preferredLabel"]
        if name in overrides:
            category = overrides[name]["category"]
            rule = f"OVERRIDE: {overrides[name]['reason']}"
        else:
            codes = ancestor_codes(uri)
            category, rule = None, None
            for rule_id, prefixes, cat in CATEGORY_RULES:
                hit = sorted(c for c in codes for p in prefixes if group_matches(c, p))
                if hit:
                    category, rule = cat, f"{rule_id} {hit[0]}"
                    break
            if category is None:
                fail(f"no category rule matches skill '{name}' (groups: {sorted(codes)})")
        if category not in VALID_CATEGORIES:
            fail(f"invalid category {category} for {name}")
        skill_rows.append({"skill_name": name, "category": category, "category_rule": rule,
                           "esco_skill_type": s["skillType"], "source_identifier": uri,
                           "description": s["description"]})

    # aliases: drop ambiguous ones and ones equal to any skill name (DATASET_SPEC §9.1)
    names_lower = {r["skill_name"].lower() for r in skill_rows}
    owner = defaultdict(set)
    for uri in skill_uris:
        for a in labels(skills_by_uri[uri]["altLabels"]):
            owner[a.lower()].add((skills_by_uri[uri]["preferredLabel"], a))
    alias_rows, dropped = [], []
    for key, owners in owner.items():
        skill_names = {n for n, _ in owners}
        if len(skill_names) > 1:
            dropped.append({"entity": "skill", "alias": key, "reason": "points to more than one skill",
                            "owners": "; ".join(sorted(skill_names))})
        elif key in names_lower:
            dropped.append({"entity": "skill", "alias": key, "reason": "equals a canonical skill name",
                            "owners": "; ".join(sorted(skill_names))})
        else:
            name, original = sorted(owners)[0]
            alias_rows.append({"skill_name": name, "alias": original})

    return (sorted(skill_rows, key=lambda r: r["skill_name"].lower()),
            sorted(alias_rows, key=lambda r: (r["skill_name"].lower(), r["alias"].lower())),
            dropped, relations, skills_by_uri)


def build_relations(relations, occupations_by_uri, skills_by_uri):
    rows = [{"occupation_name": occupations_by_uri[r["occupationUri"]]["preferredLabel"],
             "skill_name": skills_by_uri[r["skillUri"]]["preferredLabel"],
             "relation_type": r["relationType"],
             "source": f"{SOURCE_LABEL}: {r['relationType']}"} for r in relations]
    return sorted(rows, key=lambda r: (r["occupation_name"], r["relation_type"], r["skill_name"].lower()))


def write_metadata(name, description, coverage, records, processing_method, checksums, notes):
    METADATA.mkdir(parents=True, exist_ok=True)
    data = {
        # required fields (DATASET_SPEC §32, ADR 0006 §3)
        "dataset_name": name,
        "version": DATASET_VERSION,
        "source": f"{SOURCE_LABEL} (https://esco.ec.europa.eu), classification, English, CSV",
        "collection_date": DOWNLOAD_DATE,
        "coverage": coverage,
        "description": description,
        "number_of_records": records,
        "processing_method": processing_method,
        # optional fields (ADR 0006 §4)
        "processing_version": PROCESSING_VERSION,
        "schema_version": "migrations 001-021",
        "notes": notes,
        # raw file fingerprints so the same download can be verified (ADR 0010 §5)
        "source_files": checksums,
    }
    path = metadata_path(name)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"  wrote {rel(path)}")


def main() -> None:
    print(f"Building reference dataset {DATASET_VERSION} from {SOURCE_LABEL}")
    raw = load_raw()
    checksums = {name: sha256(RAW / name) for name in RAW_FILES}
    occupations_by_uri = {o["conceptUri"]: o for o in raw["occupations_en.csv"]}

    candidates = find_candidates(raw["occupations_en.csv"])
    included = apply_selection(candidates, occupations_by_uri)
    included_uris = {s["esco_uri"] for s in included}

    occ_rows, occ_alias_rows, occ_dropped = build_occupations(included, occupations_by_uri)
    skill_rows, skill_alias_rows, skill_dropped, relations, skills_by_uri = build_skills(raw, included_uris)
    rel_rows = build_relations(relations, occupations_by_uri, skills_by_uri)

    print("Writing processed files")
    write_csv(FILES["candidates"],
              ["target", "preferred_label", "matched_label", "isco_code", "decision",
               "career_family_code", "reason", "esco_uri"],
              sorted(candidates, key=lambda c: (c["target"], c["preferred_label"])))
    write_csv(FILES["occupation"],
              ["career_family_code", "occupation_name", "isco_code", "source", "source_identifier", "description"],
              occ_rows)
    write_csv(FILES["occupation_alias"], ["occupation_name", "alias"], occ_alias_rows)
    write_csv(FILES["skill"],
              ["skill_name", "category", "category_rule", "esco_skill_type", "source_identifier", "description"],
              skill_rows)
    write_csv(FILES["skill_alias"], ["skill_name", "alias"], skill_alias_rows)
    write_csv(FILES["dropped_aliases"], ["entity", "alias", "reason", "owners"],
              sorted(skill_dropped + occ_dropped, key=lambda r: (r["entity"], r["alias"])))
    write_csv(FILES["occupation_skill"],
              ["occupation_name", "skill_name", "relation_type", "source"], rel_rows)

    print("Writing metadata")
    method_occ = ("Keyword search of ESCO preferred/alternative labels for the DATASET_SPEC §38 pilot targets, "
                  "researcher review with recorded reasons (scripts/dataset/esco/occupation_selection.csv), "
                  "career family assigned in the review; ESCO altLabels kept as aliases unless ambiguous.")
    write_metadata("occupation",
                   "Pilot occupation framework (Semester 1, Web Full Stack) from ESCO",
                   "CF10 Web Development, CF11 UI/UX & Digital Product",
                   len(occ_rows), method_occ, checksums,
                   f"{len(occ_alias_rows)} aliases. Back-end / Full-stack Developer not in ESCO; "
                   "considered in Phase 3 from job postings (ADR 0010 §9).")
    write_metadata("skill",
                   "Skills related (essential or optional) to the pilot occupations in ESCO",
                   "All ESCO skills linked to the pilot occupations",
                   len(skill_rows),
                   "skill_name = ESCO preferredLabel; category by ESCO skill-hierarchy rules R1-R6 in priority order "
                   "plus reviewed overrides (scripts/dataset/esco/category_overrides.csv); aliases = ESCO altLabels "
                   "minus ambiguous ones (see datasets/processed/skill/dropped_aliases.csv).",
                   checksums,
                   f"{len(skill_alias_rows)} aliases kept, {len(skill_dropped)} dropped. "
                   "Technologies missing from ESCO (e.g. React, Node.js, Figma) are added in Phase 3.")
    write_metadata("occupation_skill",
                   "Occupation-skill relations of the pilot occupations from ESCO",
                   "Pilot occupations x related ESCO skills",
                   len(rel_rows),
                   "All ESCO relations kept without filtering; relation type stored in source "
                   "('ESCO v1.2.1: essential|optional'). importance and demand left NULL (ADR 0010 §3).",
                   checksums,
                   "demand is calculated from job postings in Phase 3 (DATASET_SPEC §24).")

    counts = {c: sum(r["category"] == c for r in skill_rows) for c in sorted(VALID_CATEGORIES)}
    print("\nSummary")
    print(f"  candidates: {len(candidates)}  included occupations: {len(occ_rows)}")
    print(f"  skills: {len(skill_rows)}  skill aliases: {len(skill_alias_rows)}  dropped aliases: {len(skill_dropped) + len(occ_dropped)}")
    print(f"  occupation aliases: {len(occ_alias_rows)}  occupation-skill relations: {len(rel_rows)}")
    print(f"  categories: {counts}")


if __name__ == "__main__":
    main()
