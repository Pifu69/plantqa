"""A kis és a nagy üzem összevetése: `uv run python -m plantqa.figures_scale`.

Bemenet: `figures/plan.json` „scale” kulcsa (melyik EXP és halmaz a kis, illetve a nagy üzem
mérése), a mérések `summary.csv` fájljai. Kimenet: `figures/scale_accuracy.png` és
`figures/scale_cost.png` (és `.pdf`), mellette az ábrák forrásadata `.csv`-ben. A színek és a
sraffozás a `plantqa.figures` szabályát követik (módszer = szín, modell = sraffozás).
"""

from __future__ import annotations

import json
from typing import Any

import matplotlib.pyplot as plt

from plantqa.figures import (
    FIGURES,
    MODEL_NAMES,
    MUTED,
    TEXT,
    _bar,
    save,
    style,
    summary_rows,
    write_csv,
)

PAIRS = [(m, mo) for mo in ("glm", "luna") for m in ("M1", "M2", "M3")]


def _rows(plan: dict[str, Any]) -> list[dict[str, Any]]:
    """Párosításonként a kis és a nagy üzem összesítő sora egy közös táblában."""
    out = []
    for size in ("small", "large"):
        item = plan["scale"][size]
        found = {(r["method"], r["model"]): r for r in summary_rows(item["exp"], item["split"])}
        for method, model in PAIRS:
            r = found.get((method, model))
            if r is None:
                continue
            out.append(
                {
                    "plant": item["label"],
                    "exp": item["exp"],
                    "split": item["split"],
                    "method": method,
                    "model": model,
                    "n": int(r["n"]),
                    "correct": int(r["correct"]),
                    "accuracy": float(r["accuracy"]),
                    "ci_low": float(r["ci_low"]),
                    "ci_high": float(r["ci_high"]),
                    "cost_per_question_usd": round(float(r["cost_usd"]) / int(r["n"]), 6),
                    "latency_median_s": float(r["latency_median_s"]),
                }
            )
    return out


def _panel(rows: list[dict[str, Any]], key: str, name: str, ylabel: str, fmt: str) -> None:
    """Párosításonként két oszlop (kis és nagy üzem), az értékek közvetlenül címkézve."""
    plants = list(dict.fromkeys(r["plant"] for r in rows))
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    width = 0.38
    labels = []
    for i, (method, model) in enumerate(PAIRS):
        labels.append(f"{method}\n{MODEL_NAMES[model]}")
        for j, plant in enumerate(plants):
            match = [
                r for r in rows if (r["method"], r["model"], r["plant"]) == (method, model, plant)
            ]
            if not match:
                continue
            value = match[0][key]
            x = i + (j - 0.5) * width
            _bar(ax, x, value, width * 0.92, method, model)
            if j == 0:
                ax.bar(x, value, width * 0.92, color="white", alpha=0.55, linewidth=0)
            text = fmt.format(value).replace(".", ",")
            ax.text(x, value, text, ha="center", va="bottom", fontsize=6.5, color=TEXT)
    ax.set_xticks(range(len(PAIRS)))
    ax.set_xticklabels(labels, fontsize=7)
    style(ax, ylabel)
    exps = " és ".join(dict.fromkeys(f"{r['plant']}: {r['exp']}" for r in rows))
    ax.set_title(
        f"Halvány oszlop: {plants[0]}, telt oszlop: {plants[-1]} — {exps}", fontsize=8, color=MUTED
    )
    save(fig, name)
    write_csv(name, rows)


def main() -> None:
    """Belépési pont."""
    plan = json.loads((FIGURES / "plan.json").read_text(encoding="utf-8"))
    rows = _rows(plan)
    _panel(rows, "accuracy", "scale_accuracy", "pontosság", "{:.2f}")
    _panel(rows, "cost_per_question_usd", "scale_cost", "költség / kérdés (USD)", "{:.4f}")
    print(f"scale figures written from {len(rows)} rows")


if __name__ == "__main__":
    main()
