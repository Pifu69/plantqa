"""Az (e) család: összetett, több adatlapos kérdések (külön mérés, EXP-030).

Minden kérdés a rajzon egy útvonalat, elemhalmazt vagy két topológiai lépést jár be, és
legalább két különböző adatlapot igényel. A referenciaválaszt program rakja össze a gold
üzemgráfból és a `data/questions/facts/gold_facts.json` tényeiből (egy vak Opus-agent gyűjtötte
a PDF-ekből, oldalszámmal). Szélsőérték vagy összevetés csak akkor kerül a referenciába, ha
minden érintett érték egyértékű és átváltható; különben a referencia a feltételtől függést
mondja ki. Futtatás: `python -m plantqa.questions.complex`.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections.abc import Iterator
from typing import Any

from plantqa.graph.sources import ROOT
from plantqa.plant import spec
from plantqa.plant.search import try_seed
from plantqa.questions.composite import steps
from plantqa.questions.sources import drawing_pool

FACTS = ROOT / "data" / "questions" / "facts" / "gold_facts.json"
OUT = spec.QUESTIONS_DIR / "complex.jsonl"
SEED = 20261031
PER_TYPE = 4
PROPERTIES = {
    "max_pressure": ("maximum allowable pressure", "lowest"),
    "max_temperature": ("maximum fluid temperature", "lowest"),
}
#: Átváltás a közös egységre (nyomás: bar, hőmérséklet: °C).
PRESSURE_TO_BAR = {
    "bar": 1.0,
    "barg": 1.0,
    "psi": 0.0689476,
    "psig": 0.0689476,
    "kpa": 0.01,
    "mpa": 10.0,
}


def facts() -> dict[str, Any]:
    """A gold tények dokumentumonként."""
    return dict(json.loads(FACTS.read_text(encoding="utf-8"))["documents"])


def tag_documents() -> dict[str, str]:
    """Tag → document_id (a programmal előállított hozzárendelés)."""
    return dict(json.loads((spec.PLANT_DIR / "tag_to_datasheet.json").read_text("utf-8")))


def normalized(value: float, unit: str) -> float | None:
    """Az érték a közös egységben (bar vagy °C); ismeretlen egységnél `None`."""
    u = unit.lower().replace(" ", "").replace("°", "").replace("deg", "")
    if u in PRESSURE_TO_BAR:
        return value * PRESSURE_TO_BAR[u]
    if u in ("c", "celsius"):
        return value
    if u in ("f", "fahrenheit"):
        return (value - 32) * 5 / 9
    return None


def describe(fact: dict[str, Any]) -> str:
    """Egy tény rövid, olvasható alakja oldalszámmal."""
    if fact.get("stated") is False:
        return "not stated in the datasheet"
    page = f" (p. {fact['page']})" if fact.get("page") else ""
    if fact.get("single_value"):
        return f"{fact['value_text']}{page}"
    cases = "; ".join(f"{v['condition']}: {v['value_text']}" for v in fact.get("values", [])[:4])
    return f"depends on the construction ({cases}){page}"


def interval(fact: dict[str, Any]) -> tuple[float, float] | None:
    """A tény összes átváltható értékének tartománya (közös egységben); ha nincs, `None`.

    Egyértékű ténynél egy pont; több esetnél az esetek értékeinek minimuma és maximuma, de csak
    ha minden eset átváltható (különben a tartomány nem megbízható).
    """
    cases = [fact] if fact.get("single_value") else list(fact.get("values", []))
    numbers = []
    for case in cases:
        if case.get("value") is None:
            return None
        value = normalized(float(case["value"]), str(case.get("unit", "")))
        if value is None:
            return None
        numbers.append(value)
    return (min(numbers), max(numbers)) if numbers else None


def decidable_lowest(ranges: dict[str, tuple[float, float]]) -> str | None:
    """Az az elem, amelynek legnagyobb értéke is kisebb minden más elem legkisebb értékénél."""
    for tag, (_, high) in ranges.items():
        if all(high < low for other, (low, _) in ranges.items() if other != tag):
            return tag
    return None


def reference(items: list[str], prop: str) -> dict[str, Any]:
    """A referencia: tagenkénti érték, és ha a tartományokból eldönthető, a legkisebb elem."""
    docs, known = tag_documents(), facts()
    per_tag = {t: known.get(docs[t], {}).get(prop, {"stated": False}) for t in items if t in docs}
    lines = [f"{t} ({docs[t]}): {describe(f)}" for t, f in per_tag.items()]
    must = [f"{t}: {describe(f).split(' (p.')[0]}" for t, f in per_tag.items()]
    ranges = {t: interval(f) for t, f in per_tag.items()}
    known_ranges = {t: r for t, r in ranges.items() if r is not None}
    lowest = decidable_lowest(known_ranges) if len(known_ranges) == len(ranges) else None
    if lowest is not None and len(ranges) >= 2:
        lines.append(f"Lowest: {lowest} (for every listed construction).")
        must.append(f"lowest: {lowest}")
    else:
        lines.append("Which one is the lowest cannot be decided from the datasheets alone.")
        must.append("says the comparison depends on the construction (not decidable as asked)")
    return {"answer": " ".join(lines), "must": must, "answerable": "yes", "per_tag": per_tag}


def with_datasheet(tags: list[str]) -> list[str]:
    """Az adatlappal rendelkező tagek, sorrend megtartva."""
    docs = tag_documents()
    return [t for t in tags if t in docs]


def _plant_seed() -> int:
    log = json.loads((spec.PLANT_DIR / "seed_search.json").read_text("utf-8"))
    return int(log["accepted_seed"])


def path_questions(rng: random.Random) -> Iterator[dict[str, Any]]:
    """Útvonal + szélsőérték: Benedek gold FLOW_PATH útjai, legalább két különböző adatlappal."""
    docs = tag_documents()
    paths = [q for q in drawing_pool() if q["family"] == "FLOW_PATH" and q["answerable"]]
    rng.shuffle(paths)
    for q in paths:
        items = with_datasheet(list(q["reference"]))
        if len({docs[t] for t in items}) < 2:
            continue
        prop = rng.choice(sorted(PROPERTIES))
        name, word = PROPERTIES[prop]
        start, end = q["anchors"]
        text = (
            f"Along the process flow path from {start} to {end}, which item has the {word} "
            f"{name} according to its datasheet? Give the value for every item on the path "
            "that has a datasheet."
        )
        yield {"kind": "path_extreme", "text": text, "tags": items, "prop": prop}


def successor_sets(rng: random.Random) -> Iterator[dict[str, Any]]:
    """Halmaz + felsorolás: egy elem közvetlen utódai, legalább két különböző adatlappal."""
    plant = try_seed(_plant_seed()).corpus.plant
    tag = {n: d.get("tag") for n, d in plant.nodes(data=True)}
    docs = tag_documents()
    flow = [(a, b) for a, b, d in plant.edges(data=True) if d.get("relation") == "send_to"]
    sources = sorted({a for a, _ in flow if tag.get(a)}, key=lambda n: str(tag[n]))
    rng.shuffle(sources)
    for src in sources:
        items = with_datasheet([str(tag[b]) for a, b in flow if a == src and tag.get(b)])
        if len({docs[t] for t in items}) < 2:
            continue
        for prop in sorted(PROPERTIES):  # kevés ilyen elem van: mindkét tulajdonságra kérdezünk
            name, word = PROPERTIES[prop]
            text = (
                f"For each item that receives flow directly from {tag[src]}, what is its {name} "
                f"according to its datasheet, and which of them has the {word}?"
            )
            yield {"kind": "set_enumerate", "text": text, "tags": sorted(items), "prop": prop}


def step_pairs(rng: random.Random) -> Iterator[dict[str, Any]]:
    """Két lépés + összevetés: két egyértelmű topológiai lépés különböző adatlapú célelemmel."""
    plant = try_seed(_plant_seed()).corpus.plant
    all_steps = steps(plant, set(tag_documents().values()))
    rng.shuffle(all_steps)
    for first, second in zip(all_steps[::2], all_steps[1::2], strict=False):
        if first.target_document == second.target_document:
            continue
        prop = rng.choice(sorted(PROPERTIES))
        name, word = PROPERTIES[prop]
        text = (
            f"Compare {first.phrase} and {second.phrase}: which of the two has the {word} "
            f"{name} according to its datasheet, and what are the two values?"
        )
        pair = [first.__dict__, second.__dict__]
        yield {"kind": "step_compare", "text": text, "tags": [first.target, second.target],
               "prop": prop, "steps": pair}  # fmt: skip


def _take(gen: Iterator[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in gen:
        if item["text"] not in seen:
            seen.add(item["text"])
            out.append(item)
        if len(out) == n:
            break
    return out


def build() -> list[dict[str, Any]]:
    """Típusonként `PER_TYPE` kérdés, a referenciával együtt."""
    rng = random.Random(SEED)
    raw = _take(path_questions(rng), PER_TYPE) + _take(successor_sets(rng), PER_TYPE)
    raw += _take(step_pairs(rng), PER_TYPE)
    docs = tag_documents()
    out = []
    for index, item in enumerate(raw, start=1):
        source = {"kind": "complex", **{k: v for k, v in item.items() if k != "text"}}
        row = {"qid": f"e{index:02d}", "split": "complex", "family": "e", "text": item["text"]}
        row |= {"answer_type": "FREE_TEXT", "gold": reference(item["tags"], item["prop"])}
        row |= {"tags": item["tags"], "documents": sorted({docs[t] for t in item["tags"]})}
        out.append({**row, "source": source})
    return out


def main() -> None:
    """Kiírás és sha256 (a futtatás előtt befagyasztva)."""
    rows = build()
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(json.dumps({"n": len(rows), "sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
