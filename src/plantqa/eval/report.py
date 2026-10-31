"""Összesítés egy mérésről: `python -m plantqa.eval.report --exp EXP-010`.

A `scored.jsonl`-ból (`score.py merge`) módszer × modell × halmaz × család bontásban:
helyes / részben / rossz / hallucinált / függő darabszám, pontosság (helyes / összes), tokenek,
költség (a szolgáltató ára, a cache-ből jövőnél is), valódi költés, késleltetés, útvonalak.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from plantqa.eval.run import RUNS

VERDICTS = ("correct", "partial", "wrong", "hallucinated", "pending")
FIELDS = [
    "exp",
    "method",
    "model",
    "split",
    "family",
    "n",
    *VERDICTS,
    "accuracy",
    "prompt_tokens",
    "completion_tokens",
    "cost_usd",
    "spent_usd",
    "latency_median_s",
    "latency_mean_s",
]


def load_scored(exp: str) -> list[dict[str, Any]]:
    """A mérés pontozott sorai."""
    path = RUNS / exp / "scored.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def summarize(exp: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Egy csoport (pl. egy módszer egy családon) összesítő sora."""
    verdicts = Counter(r["score"]["verdict"] for r in rows)
    usage = [r["answer"]["usage"] for r in rows]
    latency = [float(r["answer"]["latency_s"]) for r in rows]
    first = rows[0]
    out: dict[str, Any] = {"exp": exp, "method": first["method"], "model": first["model"]}
    out |= {"split": first["split"], "n": len(rows)}
    out |= {v: verdicts.get(v, 0) for v in VERDICTS}
    out["accuracy"] = round(verdicts.get("correct", 0) / len(rows), 4)
    for key in ("prompt_tokens", "completion_tokens"):
        out[key] = sum(int(u.get(key, 0)) for u in usage)
    for key in ("cost_usd", "spent_usd"):
        out[key] = round(sum(float(u.get(key, 0.0)) for u in usage), 6)
    out["latency_median_s"] = round(statistics.median(latency), 2)
    out["latency_mean_s"] = round(statistics.fmean(latency), 2)
    return out


def table(exp: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Csoportonként egy sor: minden családra külön, és „all” a teljes halmazra."""
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        base = (r["method"], r["model"], r["split"])
        groups[(*base, r["family"])].append(r)
        groups[(*base, "all")].append(r)
    return [{**summarize(exp, g), "family": k[3]} for k, g in sorted(groups.items())]


def routes(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Az M1/M2 útvonalainak gyakorisága (melyik tier/eszköz válaszolt)."""
    counts: Counter[tuple[str, str, str]] = Counter()
    for r in rows:
        kinds = {step.split(":")[0] for step in r["answer"]["route"]}
        counts[(r["method"], r["model"], "+".join(sorted(kinds)) or "-")] += 1
    return [{"method": m, "model": mo, "route": rt, "n": n} for (m, mo, rt), n in counts.items()]


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    """CSV kiírása a megadott oszloprendben."""
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def markdown(rows: list[dict[str, Any]]) -> str:
    """Rövid markdown-táblázat a teljes halmazokról és családonként."""
    head = "| módszer | modell | halmaz | család | n | helyes | részben | rossz | halluc. | függő |"
    head += " pontosság | költség (USD) | medián késl. (s) |\n|" + "---|" * 13
    lines = [head]
    for r in rows:
        cells = [r["method"], r["model"], r["split"], r["family"], r["n"]]
        cells += [r[v] for v in VERDICTS]
        cells += [f"{r['accuracy']:.3f}", f"{r['cost_usd']:.4f}", r["latency_median_s"]]
        lines.append("| " + " | ".join(map(str, cells)) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    """Belépési pont: `summary.csv`, `summary.md`, `routes.csv` a mérés mappájába."""
    parser = argparse.ArgumentParser(description="Summarize a scored measurement")
    parser.add_argument("--exp", required=True)
    exp = parser.parse_args().exp
    rows = load_scored(exp)
    summary = table(exp, rows)
    folder = RUNS / exp
    write_csv(folder / "summary.csv", summary, FIELDS)
    write_csv(folder / "routes.csv", routes(rows), ["method", "model", "route", "n"])
    (folder / "summary.md").write_text(markdown(summary), encoding="utf-8")
    print(markdown([r for r in summary if r["family"] == "all"]))


if __name__ == "__main__":
    main()
