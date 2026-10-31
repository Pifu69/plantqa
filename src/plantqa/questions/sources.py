"""A kérdések forrásai: Benedek generátorának készlete és a plantdocs kérdés-válasz párjai."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from plantqa.graph.sources import PLANTDOCS, ROOT

EXPERIMENTS = PLANTDOCS / "docs" / "private" / "30-experiments"
#: A plantdocs gold kérdés-válasz párjai eszközönként (EXP-0026: 25/eszköz, EXP-0039: 200).
PLANTDOCS_SETS = {
    "gorman-rupp-0700286": EXPERIMENTS / "EXP-0026-mintakerdesek" / "gorman-rupp-0700286.json",
    "fisher-et-d100022x012": EXPERIMENTS / "EXP-0026-mintakerdesek" / "fisher-et-d100022x012.json",
    "gfps-165-solenoid-valve": EXPERIMENTS
    / "EXP-0026-mintakerdesek"
    / "gfps-165-solenoid-valve.json",
    "rosemount-3051-00813-0100-4001": EXPERIMENTS
    / "EXP-0039-rosemount-kerdesek"
    / "rosemount-3051-00813-0100-4001.json",
}
DRAWING_POOL = ROOT / "data" / "questions" / "pool_a" / "questions.jsonl"


def drawing_pool(path: Path = DRAWING_POOL) -> list[dict[str, Any]]:
    """Benedek generátorának kérdései a PQA korpuszon (gold válasszal)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def datasheet_questions(document_id: str) -> list[dict[str, Any]]:
    """Egy eszköz plantdocs-kérdései, a forrásfájl nevével kiegészítve."""
    path = PLANTDOCS_SETS[document_id]
    questions = json.loads(path.read_text(encoding="utf-8"))["questions"]
    source = str(path.relative_to(PLANTDOCS))
    return [{**q, "document_id": document_id, "source_file": source} for q in questions]
