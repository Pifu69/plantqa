"""A kérdéssor összeállítása (program, seedelt): `python -m plantqa.questions.build`.

Négy család, családonként 15 kérdés: (a) csak rajz — Benedek generátorának kérdései;
(b) csak adatlap, tagen át — a plantdocs EXP-0026/EXP-0039 gold párjai a tagre leképezve;
(c) összetett — egy egyértelmű topológiai lépés és egy (b)-típusú adatlapi kérdés, a gold
programmal összerakva; (d) megválaszolhatatlan — nem létező tag, a dokumentumban nem szereplő
tény, illetve ilyen tény topológiai lépésen át. Családonként 5 kérdés dev, 10 teszt.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import defaultdict
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

from plantqa.graph.sources import ROOT
from plantqa.plant.search import try_seed
from plantqa.questions.composite import Step, steps
from plantqa.questions.sources import PLANTDOCS_SETS, datasheet_questions, drawing_pool

SEED = 20261031
PER_FAMILY = 15
DEV_PER_FAMILY = 5
OUT_DIR = ROOT / "data" / "questions"
NOT_IN_DOCUMENTS = "Not in the documents."
#: Az összetett kérdésekhez a jól ellenőrizhető kategóriák (egy adott érték vagy feltétel).
FACT_CATEGORIES = {"value", "conditional", "multi_condition", "footnote", "limit_check", "list"}


def _tags_by_document() -> dict[str, list[str]]:
    mapping = json.loads((ROOT / "data/plant/tag_to_datasheet.json").read_text("utf-8"))
    out: dict[str, list[str]] = defaultdict(list)
    for tag, doc in sorted(mapping.items()):
        out[doc].append(tag)
    return dict(out)


def _plant_seed() -> int:
    log = json.loads((ROOT / "data/plant/seed_search.json").read_text("utf-8"))
    return int(log["accepted_seed"])


def _round_robin(groups: dict[str, list[Any]], n: int) -> list[Any]:
    """Felváltva választ a csoportokból (névsorrendben), amíg `n` elem össze nem jön."""
    queues = {k: list(v) for k, v in sorted(groups.items())}
    picked: list[Any] = []
    while len(picked) < n and any(queues.values()):
        for key in list(queues):
            if queues[key] and len(picked) < n:
                picked.append(queues[key].pop(0))
    return picked


def drawing_family(rng: random.Random) -> list[dict[str, Any]]:
    """(a) A generátor kérdései (a megválaszolhatatlanok nélkül), családonként felváltva."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for q in drawing_pool():
        if q["answerable"] and q["family"] != "UNANSWERABLE_TAG":
            groups[q["family"]].append(q)
    for items in groups.values():
        rng.shuffle(items)
    return [_drawing_item(q, "a") for q in _round_robin(groups, PER_FAMILY)]


def _drawing_item(q: dict[str, Any], family: str) -> dict[str, Any]:
    gold = {"answer": q["reference"], "answerable": q["answerable"]}
    return {
        "family": family,
        "text": q["text"],
        "answer_type": q["answer_type"],
        "gold": gold,
        "tags": q["anchors"],
        "documents": [],
        "source": {"kind": "plantgraph", "question_id": q["question_id"], "pg": q},
    }


def _fact_pool(rng: random.Random, answerable: str) -> dict[str, list[dict[str, Any]]]:
    """Eszközönként a megfelelő plantdocs-kérdések, keverve."""
    pools = {}
    for doc in sorted(PLANTDOCS_SETS):
        items = [q for q in datasheet_questions(doc) if q["answerable"] == answerable]
        reserve: list[dict[str, Any]] = []
        if answerable == "yes":
            items = [q for q in items if q["category"] in FACT_CATEGORIES]
            # tartalék: a részben megválaszolható kérdések a teljesen megválaszolhatók után
            reserve = [q for q in datasheet_questions(doc) if q["answerable"] == "partial"]
            rng.shuffle(reserve)
        rng.shuffle(items)
        pools[doc] = items + reserve
    return pools


def _gold_of(q: dict[str, Any]) -> dict[str, Any]:
    keys = ("answer", "must", "tolerance", "answerable", "category")
    gold = {k: q[k] for k in keys if k in q}
    if q["answerable"] == "no":
        gold["expected"] = NOT_IN_DOCUMENTS
    return gold


def _source(q: dict[str, Any]) -> dict[str, Any]:
    return {"kind": "plantdocs", "question_id": q["id"], "file": q["source_file"]}


def tag_item(q: dict[str, Any], tag: str, family: str) -> dict[str, Any]:
    """(b)/(d) Egy plantdocs-kérdés a tagre leképezve."""
    return {
        "family": family,
        "text": f"Regarding {tag} on the P&ID: {q['question']}",
        "answer_type": "FREE_TEXT",
        "gold": _gold_of(q),
        "tags": [tag],
        "documents": [q["document_id"]],
        "source": _source(q),
    }


def composite_item(q: dict[str, Any], step: Step, family: str) -> dict[str, Any]:
    """(c)/(d) Topológiai lépés + adatlapi kérdés; a gold a köztes tag és a plantdocs gold."""
    gold = {**_gold_of(q), "via_tag": step.target, "relation": step.relation}
    return {
        "family": family,
        "text": f"Consider {step.phrase}. {q['question']}",
        "answer_type": "FREE_TEXT",
        "gold": gold,
        "tags": [step.anchor, step.target],
        "documents": [step.target_document],
        "source": {**_source(q), "step": step.__dict__},
    }


def _cycle(items: list[str]) -> Iterator[str]:
    while True:
        yield from items


def datasheet_family(pools: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """(b) Eszközönként felváltva, a tageket körbejárva."""
    tags = {doc: _cycle(t) for doc, t in _tags_by_document().items()}
    picked = _round_robin({d: [(d, q) for q in qs] for d, qs in pools.items()}, PER_FAMILY)
    for doc, q in picked:
        pools[doc].remove(q)
    return [tag_item(q, next(tags[doc]), "b") for doc, q in picked]


def composite_family(
    pools: dict[str, list[dict[str, Any]]], plant_steps: list[Step], n: int, family: str
) -> list[dict[str, Any]]:
    """(c) vagy (d): lépésenként egy, a lépés cél-eszközének következő kérdésével."""
    by_relation: dict[str, list[Step]] = defaultdict(list)
    for step in plant_steps:
        by_relation[step.relation].append(step)
    out = []
    for step in _round_robin(dict(by_relation), len(plant_steps)):
        if pools[step.target_document] and len(out) < n:
            out.append(composite_item(pools[step.target_document].pop(0), step, family))
    return out


def unanswerable_family(rng: random.Random, plant_steps: list[Step]) -> list[dict[str, Any]]:
    """(d) 5 nem létező tag (Benedek), 6 dokumentumban nem szereplő tény, 4 lépésen át."""
    drawing = [q for q in drawing_pool() if q["family"] == "UNANSWERABLE_TAG"]
    rng.shuffle(drawing)
    items = [_drawing_item(q, "d") for q in drawing[:5]]
    for item in items:
        item["gold"]["expected"] = NOT_IN_DOCUMENTS
    pools = _fact_pool(rng, "no")
    tags = {doc: _cycle(t) for doc, t in _tags_by_document().items()}
    picked = _round_robin({d: [(d, q) for q in qs] for d, qs in pools.items()}, 6)
    for doc, q in picked:
        pools[doc].remove(q)
        items.append(tag_item(q, next(tags[doc]), "d"))
    shuffled = list(plant_steps)
    rng.shuffle(shuffled)
    return items + composite_family(pools, shuffled, 4, "d")


def build() -> list[dict[str, Any]]:
    """Mind a 60 kérdés, azonosítóval és dev/teszt besorolással."""
    rng = random.Random(SEED)
    plant_steps = steps(try_seed(_plant_seed()).corpus.plant, set(PLANTDOCS_SETS))
    pools = _fact_pool(rng, "yes")
    families: list[Callable[[], list[dict[str, Any]]]] = [
        lambda: drawing_family(rng),
        lambda: datasheet_family(pools),
        lambda: composite_family(pools, plant_steps, PER_FAMILY, "c"),
        lambda: unanswerable_family(rng, plant_steps),
    ]
    questions: list[dict[str, Any]] = []
    for make in families:
        items = make()
        rng.shuffle(items)
        for index, item in enumerate(items):
            split = "dev" if index < DEV_PER_FAMILY else "test"
            questions.append({"qid": f"{item['family']}{index + 1:02d}", "split": split, **item})
    return questions


def write(questions: list[dict[str, Any]], out_dir: Path = OUT_DIR) -> dict[str, str]:
    """`dev.jsonl` és `test.jsonl` kiírása; a visszatérési érték a fájlok sha256-ja."""
    hashes = {}
    for split in ("dev", "test"):
        rows = [q for q in questions if q["split"] == split]
        text = "".join(json.dumps(q, ensure_ascii=False, sort_keys=True) + "\n" for q in rows)
        path = out_dir / f"{split}.jsonl"
        path.write_text(text, encoding="utf-8", newline="\n")
        hashes[split] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return hashes


def main() -> None:
    """Belépési pont: összeállít, kiír, és kiírja a hash-eket és a családonkénti számokat."""
    questions = build()
    hashes = write(questions)
    counts: dict[str, int] = defaultdict(int)
    for q in questions:
        counts[f"{q['family']}:{q['split']}"] += 1
    print(json.dumps({"sha256": hashes, "counts": dict(sorted(counts.items()))}, indent=2))


if __name__ == "__main__":
    main()
