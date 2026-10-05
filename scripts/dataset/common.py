"""Shared settings and helpers for the scripts in scripts/dataset/.

Used by build_esco_reference.py, validate.py and import.py so the dataset
version, paths and allowed values are defined in one place.
Standard library only (ADR 0010 §6).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

# ---------------------------------------------------------------- versions
ESCO_VERSION = "v1.2.1"
DOWNLOAD_DATE = "2026-10-05"           # date the ESCO package was downloaded
DATASET_VERSION = "2026.01"            # ADR 0010 §4: YYYY.NN
SOURCE_LABEL = f"ESCO {ESCO_VERSION}"  # value of occupation.source

# ---------------------------------------------------------------- paths
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "datasets" / "raw" / "esco" / ESCO_VERSION
CONFIG = Path(__file__).resolve().parent / "esco"
PROCESSED = ROOT / "datasets" / "processed"
METADATA = ROOT / "datasets" / "metadata"
SEED_REFERENCE = ROOT / "database" / "seed" / "reference"

# ---------------------------------------------------------------- allowed values
# chk_skill_category (migration 005, DATABASE.md §15)
VALID_CATEGORIES = {"TECHNICAL", "DESIGN", "CREATIVE", "SOFTWARE_TOOL",
                    "COMMUNICATION", "BUSINESS", "OTHER"}

# ESCO occupation-skill relation types (ADR 0010 §11)
RELATION_TYPES = {"essential", "optional"}

# Initial Candidate Career Families (DATABASE.md §19)
CAREER_FAMILIES = [
    ("CF01", "Film & Video Production"),
    ("CF02", "Post-Production & Motion/VFX"),
    ("CF03", "Broadcast & Audio"),
    ("CF04", "Advertising & Creative"),
    ("CF05", "Digital Marketing & Content"),
    ("CF06", "PR & Corporate Communication"),
    ("CF07", "Graphic & Visual Communication"),
    ("CF08", "Packaging & Print Design"),
    ("CF09", "Prepress & Print Production"),
    ("CF10", "Web Development"),
    ("CF11", "UI/UX & Digital Product"),
    ("CF12", "Web Content & Growth"),
    ("CF13", "Game Design & Production"),
    ("CF14", "Game Development & Technical"),
    ("CF15", "Game Art & Animation"),
]

# Processed files and metadata of this dataset version (ADR 0006)
FILES = {
    "candidates": PROCESSED / "occupation" / "esco_candidates.csv",
    "occupation": PROCESSED / "occupation" / "occupation.csv",
    "occupation_alias": PROCESSED / "occupation" / "occupation_alias.csv",
    "skill": PROCESSED / "skill" / "skill.csv",
    "skill_alias": PROCESSED / "skill" / "skill_alias.csv",
    "dropped_aliases": PROCESSED / "skill" / "dropped_aliases.csv",
    "occupation_skill": PROCESSED / "occupation_skill" / "occupation_skill.csv",
}
METADATA_DATASETS = ["occupation", "skill", "occupation_skill"]


def metadata_path(dataset_name: str) -> Path:
    return METADATA / f"{dataset_name}_{DATASET_VERSION}.json"


# ---------------------------------------------------------------- helpers
def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def rel(path: Path) -> str:
    """Path relative to the repository root, with forward slashes."""
    return path.relative_to(ROOT).as_posix()
