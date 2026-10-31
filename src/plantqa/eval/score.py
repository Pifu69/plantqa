"""Pontozás: ahol lehet, programmal; a maradék vak bírálatra megy (Claude Code subagentek).

- (a) és a rajzos (d): Benedek `score_answer`-e (tagek halmaza, út, szám, igen/nem, abstain).
- Szabad szöveges kérdés, megválaszolható: ha a válasz „nincs benne”, programmal rossz
  (hamis tartózkodás, Benedek szabálya), kivéve ha mellette szöveges választ is adott; ha a
  gold minden `must` eleme számot tartalmaz, és minden szám a mértékegységével együtt szerepel
  a válaszban, programmal helyes; különben bíráló.
- Szabad szöveges, megválaszolhatatlan: ha a válasz „nincs benne”, programmal helyes; különben
  bíráló (lehet, hogy szövegben mondja, hogy nincs benne, vagy kitalál valamit).
A bírálati csomag vak: a tételek sorrendje kevert, az azonosító nem árulja el a módszert és a
modellt; a kulcs külön fájlban van.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from functools import cache
from pathlib import Path
from typing import Any

from plantgraph.qa.corpus import load_corpus_artifacts
from plantgraph.qa.graph_view import NetworkxGraphView
from plantgraph.qa.harness.gold import GoldScoring, build_gold_scoring
from plantgraph.qa.models import FinalAnswer, Outcome
from plantgraph.qa.models import Question as PgQuestion
from plantgraph.qa.scoring import score_answer

from plantqa.eval.run import RUNS, load_questions
from plantqa.methods.base import answer_text

NUMBER = re.compile(r"(?<![\w.])[-+]?\d+(?:[.,]\d+)*(?:\s*/\s*\d+)?")
UNIT_AFTER = re.compile(r"[-+]?\d+(?:[.,]\d+)*(?:\s*/\s*\d+)?\s*([A-Za-z%°µ\"]+[A-Za-z/²³]*)")
SEED = 20261031
SPLITS = ("dev", "test", "complex")
BATCH = 40


def _numbers(text: str) -> set[str]:
    return {n.replace(",", "").replace(" ", "") for n in NUMBER.findall(text)}


def numeric_match(must: list[str], answer: str) -> bool | None:
    """Minden `must` elem száma (és utána álló egysége) szerepel-e; `None`: nem programozható."""
    if not must or any(not NUMBER.search(item) for item in must):
        return None
    found, lower = _numbers(answer), answer.lower()
    for item in must:
        if not _numbers(item) <= found:
            return False
        units = [u.lower() for u in UNIT_AFTER.findall(item)]
        if any(unit not in lower for unit in units):
            return False
    return True


@cache
def gold_scoring() -> GoldScoring:
    """Benedek harnessének útvonal-pontozási bemenete: a gold `send_to` élek és a csatlakozók."""
    from plantqa.graph.load import INGEST_JSON
    from plantqa.plant.search import try_seed
    from plantqa.plant.spec import CORPUS_ID
    from plantqa.questions.build import _plant_seed

    a = load_corpus_artifacts(CORPUS_ID, INGEST_JSON)
    view = NetworkxGraphView(CORPUS_ID, a.localized_sheets, a.resolution)
    return build_gold_scoring(try_seed(_plant_seed()).corpus.plant, view)


def _drawing_score(question: dict[str, Any], answer: dict[str, Any]) -> dict[str, Any]:
    pg = PgQuestion.model_validate(question["source"]["pg"])
    final = answer.get("final")
    outcome = Outcome.ANSWERED if final else Outcome.PARSE_FAILURE
    parsed = FinalAnswer.model_validate(final) if final else None
    try:
        gold = gold_scoring()
        scored = score_answer(
            pg,
            outcome,
            parsed,
            connector_tags=gold.connector_tags,
            valid_edges=gold.valid_edges,
        )
    except (ValueError, TypeError) as error:
        return {"source": "program", "verdict": "wrong", "detail": f"unscorable: {error}"}
    return {"source": "program", "verdict": "correct" if scored.correct else "wrong"}


def program_score(question: dict[str, Any], answer: dict[str, Any]) -> dict[str, Any] | None:
    """A programmal eldönthető ítélet, vagy `None` (bírálóra megy)."""
    if question["source"]["kind"] == "plantgraph":
        return _drawing_score(question, answer)
    final = answer.get("final") or {}
    abstained = bool(final.get("not_present"))
    answerable = question["gold"].get("answerable") != "no"
    has_text = bool(str(final.get("answer") or "").strip())
    if abstained and has_text:
        return None  # „nincs benne” jelzés mellett is válaszolt: a bíráló dönt
    if abstained:
        verdict = "wrong" if answerable else "correct"
        return {"source": "program", "verdict": verdict, "detail": "not_present"}
    if not answerable or not final:
        return None
    match = numeric_match(question["gold"].get("must") or [], str(final.get("answer")))
    return {"source": "program", "verdict": "correct", "detail": "numeric"} if match else None


def candidate_text(answer: dict[str, Any]) -> str:
    """A bírálónak mutatott válasz: a végső válasz szövege, vagy hogy nem született válasz."""
    final = answer.get("final")
    if not final:
        return f"(no answer: {answer.get('outcome')})"
    return answer_text(final)


def load_answers(folder: Path) -> list[dict[str, Any]]:
    """A mérés minden válaszsora, a forrásfájl nevével."""
    rows = []
    for path in sorted(folder.glob("M?-*-*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append({**json.loads(line), "file": path.name})
    return rows


def score_folder(exp: str) -> list[dict[str, Any]]:
    """Programos pontozás; a bírálandó tételek `score` mezője `None`."""
    questions = {q["qid"]: q for split in SPLITS for q in load_questions(split)}
    rows = load_answers(RUNS / exp)
    for row in rows:
        row["score"] = program_score(questions[row["qid"]], row["answer"])
    return rows


def export_judge(exp: str) -> int:
    """A bírálandó tételek vak csomagja (`judge/items-N.json`) és a kulcs (`judge/key.json`)."""
    questions = {q["qid"]: q for split in SPLITS for q in load_questions(split)}
    pending = [r for r in score_folder(exp) if r["score"] is None]
    random.Random(SEED).shuffle(pending)
    folder = RUNS / exp / "judge"
    folder.mkdir(parents=True, exist_ok=True)
    key_path = folder / "key.json"
    key = json.loads(key_path.read_text(encoding="utf-8")) if key_path.exists() else {}
    first = len(list(folder.glob("items-*.json")))
    items = []
    for row in pending:
        ident = hashlib.sha256(f"{exp}|{row['file']}|{row['qid']}".encode()).hexdigest()[:10]
        if ident in key:
            continue  # már kiadott tétel: a korábbi csomagban van
        key[ident] = {"file": row["file"], "qid": row["qid"]}
        gold = dict(questions[row["qid"]]["gold"])
        gold["question"] = questions[row["qid"]]["text"]
        items.append({"item": ident, "gold": gold, "candidate": candidate_text(row["answer"])})
    for start in range(0, len(items), BATCH):
        part = folder / f"items-{first + start // BATCH + 1}.json"
        text = json.dumps(items[start : start + BATCH], indent=1, ensure_ascii=False)
        part.write_text(text, encoding="utf-8")
    key_path.write_text(json.dumps(key, indent=1), encoding="utf-8")
    return len(items)


def export_rejudge(exp: str) -> int:
    """Újrabírálat: a „nincs benne” + szöveg tételek, amelyeket a régi exportszöveg elrejtett.

    A régi `candidate_text` ilyenkor csak „Not in the documents.”-t mutatott a bírálónak; a
    tételek a javított szöveggel `judge/items-r1.json`-ba kerülnek, az új ítéletek
    (`verdicts-r1.json`) a betűrend miatt felülírják a régieket az összefésülésnél.
    """
    questions = {q["qid"]: q for split in SPLITS for q in load_questions(split)}
    folder = RUNS / exp / "judge"
    key = json.loads((folder / "key.json").read_text(encoding="utf-8"))
    by_row = {(v["file"], v["qid"]): ident for ident, v in key.items()}
    items = []
    for row in load_answers(RUNS / exp):
        final = row["answer"].get("final") or {}
        ident = by_row.get((row["file"], row["qid"]))
        if ident is None or not final.get("not_present") or not str(final.get("answer") or ""):
            continue
        gold = {**questions[row["qid"]]["gold"], "question": questions[row["qid"]]["text"]}
        items.append({"item": ident, "gold": gold, "candidate": candidate_text(row["answer"])})
    random.Random(SEED).shuffle(items)
    text = json.dumps(items, indent=1, ensure_ascii=False)
    (folder / "items-r1.json").write_text(text, encoding="utf-8")
    return len(items)


def merged(exp: str) -> list[dict[str, Any]]:
    """Programos és bírálói ítéletek együtt (a hiányzó bírálat `pending`)."""
    folder = RUNS / exp / "judge"
    key = json.loads((folder / "key.json").read_text("utf-8")) if folder.exists() else {}
    verdicts: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(folder.glob("verdicts-*.json")) if folder.exists() else []:
        for v in json.loads(path.read_text(encoding="utf-8")):
            where = key[v["item"]]
            verdicts[(where["file"], where["qid"])] = {"source": "judge", **v}
    rows = score_folder(exp)
    for row in rows:
        if row["score"] is None:
            row["score"] = verdicts.get((row["file"], row["qid"]), {"verdict": "pending"})
    return rows


def main() -> None:
    """`export` (bírálati csomag), `rejudge` (újrabírálat) vagy `merge` (`scored.jsonl`)."""
    parser = argparse.ArgumentParser(description="Score a measurement")
    parser.add_argument("command", choices=["export", "rejudge", "merge"])
    parser.add_argument("--exp", required=True)
    args = parser.parse_args()
    if args.command == "export":
        print(f"{export_judge(args.exp)} items to judge")
        return
    if args.command == "rejudge":
        print(f"{export_rejudge(args.exp)} items to re-judge")
        return
    rows = merged(args.exp)
    out = RUNS / args.exp / "scored.jsonl"
    text = "".join(json.dumps(r, ensure_ascii=False, default=str) + "\n" for r in rows)
    out.write_text(text, encoding="utf-8")
    pending = sum(1 for r in rows if r["score"]["verdict"] == "pending")
    print(f"{len(rows)} rows, {pending} pending -> {out}")


if __name__ == "__main__":
    main()
