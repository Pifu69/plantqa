"""A példaüzem legenerálása és kiírása: `python -m plantqa.plant.generate`.

Kimenet (`data/plant/`): `corpora/PQA/ingest.json` (Benedek ingest-rekordja, ebből építi újra
a korpuszt a QA, a rajzexport és a betöltő), `tag_to_datasheet.json`, `tags.json` (minden
tagelt elem, az adatlap nélküliek indoklással) és `seed_search.json` (a kipróbált seedek).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Final, Literal

from plantgraph.ingest.pipeline import run_synthetic

from plantqa.plant import spec
from plantqa.plant.datasheets import tag_rows, tag_to_datasheet
from plantqa.plant.search import try_seed

ROOT = Path(__file__).resolve().parents[3]
PLANT_DIR = ROOT / "data" / "plant"
CORPORA_ROOT = PLANT_DIR / "corpora"
STORE_PROFILE: Final[Literal["plant_lines"]] = "plant_lines"


def search_log(start: int, limit: int) -> tuple[int, list[dict[str, Any]]]:
    """Seedek kipróbálása sorban az első elfogadottig; a napló minden próbát tartalmaz."""
    log: list[dict[str, Any]] = []
    for seed in range(start, start + limit):
        candidate = try_seed(seed)
        log.append({"seed": seed, "failures": candidate.failures})
        if not candidate.failures:
            return seed, log
    raise RuntimeError(f"no accepted seed in [{start}, {start + limit})")


def write_json(path: Path, payload: Any) -> None:
    """JSON kiírása UTF-8-ban, olvasható behúzással."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def generate(start: int = 1, limit: int = 500) -> int:
    """Az elfogadott seed üzemének kiírása; a visszatérési érték a seed."""
    seed, log = search_log(start, limit)
    result = run_synthetic(
        corpus_id=spec.CORPUS_ID,
        generator_config=spec.generator_config(seed),
        split_config=spec.split_config(seed),
        check=True,
        settings=None,
        store_profile=STORE_PROFILE,
    )
    if not result.gate_equal:
        raise RuntimeError(f"gate G1 failed: {result.gate_differences[:5]}")
    out = CORPORA_ROOT / spec.CORPUS_ID / "ingest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    plant = try_seed(seed).corpus.plant
    write_json(PLANT_DIR / "tag_to_datasheet.json", tag_to_datasheet(plant))
    write_json(PLANT_DIR / "tags.json", tag_rows(plant))
    write_json(PLANT_DIR / "seed_search.json", {"accepted_seed": seed, "tried": log})
    return seed


def main() -> None:
    """Belépési pont."""
    parser = argparse.ArgumentParser(description="Generate the example plant")
    parser.add_argument("--start-seed", type=int, default=1)
    args = parser.parse_args()
    seed = generate(args.start_seed)
    print(f"accepted seed {seed}; written to {PLANT_DIR}")


if __name__ == "__main__":
    main()
