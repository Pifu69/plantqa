"""Egy mérés: egy módszer × egy QA-modell × egy kérdéshalmaz.

`python -m plantqa.eval.run --exp EXP-010 --method M1 --model glm --split dev [--allow-paid]`
Kimenet: `runs/<EXP>/<módszer>-<modell>-<halmaz>.jsonl` (kérdésenként a válasz, az útvonal,
a tokenek, a költség és a késleltetés) és `runs/<EXP>/meta.json`. A már megválaszolt kérdést
újrafuttatáskor kihagyja; fizetős hívás csak `--allow-paid` kapcsolóval, és 18 USD felett nem.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from plantqa import costlog
from plantqa.graph.sources import ROOT
from plantqa.llm.pins import ModelKey, pin
from plantqa.methods.base import Method, Question
from plantqa.plant import spec

RUNS = ROOT / "runs"
QUESTIONS = spec.QUESTIONS_DIR


def build_method(name: str, model: ModelKey, allow_paid: bool) -> Method:
    """A módszer példánya (lusta import: csak a kért módszer töltődik be)."""
    if name == "M1":
        from plantqa.methods.m1 import M1

        return M1(model, allow_paid)
    if name == "M2":
        from plantqa.methods.m2 import M2

        return M2(model, allow_paid)
    from plantqa.methods.m3 import M3

    return M3(model, allow_paid)


def load_questions(split: str) -> list[dict[str, Any]]:
    """A kérdéshalmaz sorai."""
    path = QUESTIONS / f"{split}.jsonl"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def as_question(row: dict[str, Any]) -> Question:
    """A módszerek bemenete; a címke Benedek kérdéscsaládja (a cascade útválasztásához)."""
    family = row["source"].get("pg", {}).get("family")
    return Question(row["qid"], row["text"], row["answer_type"], family)


def done_ids(path: Path) -> set[str]:
    """A fájlban már megválaszolt kérdések azonosítói."""
    if not path.exists():
        return set()
    lines = path.read_text(encoding="utf-8").splitlines()
    return {json.loads(line)["qid"] for line in lines if line.strip()}


def write_meta(folder: Path, args: argparse.Namespace) -> None:
    """A futás leírása: parancs, commit, modell ID, idő (a meglévőkhöz fűzve)."""
    path = folder / "meta.json"
    meta = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"runs": []}
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    meta["runs"].append(
        {
            "command": " ".join(["python -m plantqa.eval.run", *sys.argv[1:]]),
            "method": args.method,
            "model_id": pin(args.model).model_id,
            "split": args.split,
            "git_commit": commit.stdout.strip(),
            "started": datetime.now(UTC).isoformat(timespec="seconds"),
            "spent_before_usd": round(costlog.spent_usd(), 4),
        }
    )
    path.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def run(args: argparse.Namespace) -> Path:
    """A kérdések megválaszolása sorban; minden válasz azonnal a fájlba kerül."""
    if args.allow_paid:
        costlog.check_new_run()
    folder = RUNS / args.exp
    folder.mkdir(parents=True, exist_ok=True)
    out: Path = folder / f"{args.method}-{args.model}-{args.split}.jsonl"
    write_meta(folder, args)
    method = build_method(args.method, args.model, args.allow_paid)
    rows = [r for r in load_questions(args.split) if r["qid"] not in done_ids(out)]
    for row in rows:
        answer = method.ask(as_question(row))
        record = {"qid": row["qid"], "family": row["family"], "split": row["split"]}
        record |= {"method": args.method, "model": args.model, "answer": answer.as_dict()}
        with out.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        preview = ascii(answer.text()[:80])  # a Windows-konzol kódlapja nem minden jelet ír ki
        print(f"{row['qid']} {answer.outcome} {preview}", flush=True)
    return out


def main() -> None:
    """Belépési pont."""
    parser = argparse.ArgumentParser(description="Run one method on one question split")
    parser.add_argument("--exp", required=True)
    parser.add_argument("--method", choices=["M1", "M2", "M3"], required=True)
    parser.add_argument("--model", choices=["glm", "luna"], required=True)
    parser.add_argument("--split", choices=["dev", "test", "complex"], required=True)
    parser.add_argument("--allow-paid", action="store_true")
    print(run(parser.parse_args()))


if __name__ == "__main__":
    main()
