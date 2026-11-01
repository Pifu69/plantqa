"""A mérőüzemek összevetése méret szerint: `uv run python -m plantqa.figures_scale`.

Bemenet: `figures/plan.json` „scale” kulcsa (a mérőüzemek listája méret szerint növekvő
sorrendben: EXP, halmaz, címke), a mérések `summary.csv` fájljai. A hiányzó párosítás (a 1000
lapos üzemen az M3, amelynek promptja nem fér a modellek kontextusába) „n. a.” jelölést kap.
Kimenet: `figures/scale_accuracy.png` és
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
    """Párosításonként minden mérőüzem összesítő sora egy közös táblában."""
    out = []
    for item in plan["scale"]:
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
    """Párosításonként üzemenként egy oszlop (a halványtól a teltig), közvetlen címkével."""
    plants = list(dict.fromkeys(r["plant"] for r in rows))
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    width = 0.8 / len(plants)
    labels = []
    for i, (method, model) in enumerate(PAIRS):
        labels.append(f"{method}\n{MODEL_NAMES[model]}")
        for j, plant in enumerate(plants):
            match = [
                r for r in rows if (r["method"], r["model"], r["plant"]) == (method, model, plant)
            ]
            x = i + (j - (len(plants) - 1) / 2) * width
            if not match:
                ax.text(x, 0, "n. a.", ha="center", va="bottom", fontsize=5.5, color=MUTED)
                continue
            value = match[0][key]
            _bar(ax, x, value, width * 0.92, method, model)
            fade = 0.6 * (len(plants) - 1 - j) / max(len(plants) - 1, 1)
            if fade:
                ax.bar(x, value, width * 0.92, color="white", alpha=fade, linewidth=0)
            text = fmt.format(value).replace(".", ",")
            ax.text(x, value, text, ha="center", va="bottom", fontsize=5, color=TEXT)
    ax.set_xticks(range(len(PAIRS)))
    ax.set_xticklabels(labels, fontsize=7)
    style(ax, ylabel)
    order = ", ".join(plants)
    ax.set_title(f"Halványtól a teltig: {order}", fontsize=7, color=MUTED)
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
