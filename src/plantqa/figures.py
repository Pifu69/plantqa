"""Minden ábra egy paranccsal az eredményfájlokból: `uv run python -m plantqa.figures`.

Bemenet: `figures/plan.json` (mely EXP-ek a dev iterációk és melyik a végső teszt), a mérések
`summary.csv`/`routes.csv` fájljai és a betöltési jelentés. Kimenet: `figures/<név>.png` és
`.pdf`, mellette az ábra forrásadata `figures/<név>.csv`. A mérés azonosítója a forrásadatban
(`.csv`) szerepel, a feliratban nem.
Színek: a dataviz-skill alap kategorikus palettájának első három helye (módszerenként; mindhárom
pár validált), a modell sraffozással is meg van különböztetve, az értékek közvetlenül címkézve.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from plantqa.graph.sources import ROOT  # noqa: E402

FIGURES = ROOT / "figures"
RUNS = ROOT / "runs"
METHOD_COLORS = {"M1": "#2a78d6", "M2": "#eb6834", "M3": "#1baf7a"}
MODEL_HATCH = {"glm": "", "luna": "///"}
MODEL_NAMES = {"glm": "GLM-5.3 Flash", "luna": "GPT-6 Luna"}
FAMILY_NAMES = {
    "a": "(a) csak rajz",
    "b": "(b) csak adatlap",
    "c": "(c) összetett",
    "d": "(d) megválaszolhatatlan",
    "all": "összesen",
}
ROUTE_SHADES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6"]
TEXT = "#0b0b0b"
MUTED = "#52514e"
GRID = "#e4e3df"


def read_csv(path: Path) -> list[dict[str, str]]:
    """CSV-sorok szótárként."""
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(name: str, rows: list[dict[str, Any]]) -> None:
    """Az ábra forrásadata az ábra mellé."""
    if not rows:
        return
    with (FIGURES / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def style(ax: Any, ylabel: str) -> None:
    """Halvány rács és tengelyek, szöveg a szövegszínnel."""
    ax.set_ylabel(ylabel, color=MUTED)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(colors=MUTED)


def save(fig: Any, name: str) -> None:
    """PNG (300 dpi) és PDF."""
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGURES / f"{name}.{ext}", dpi=300)
    plt.close(fig)


def summary_rows(exp: str, split: str, family: str = "all") -> list[dict[str, str]]:
    """Egy mérés összesítő sorai egy halmazra és családra."""
    path = RUNS / exp / "summary.csv"
    if not path.exists():
        return []
    return [r for r in read_csv(path) if r["split"] == split and r["family"] == family]


def _keys(rows: list[dict[str, str]]) -> list[tuple[str, str]]:
    return sorted({(r["method"], r["model"]) for r in rows})


def _bar(ax: Any, x: float, value: float, width: float, method: str, model: str) -> None:
    ax.bar(
        x,
        value,
        width,
        color=METHOD_COLORS[method],
        hatch=MODEL_HATCH[model],
        edgecolor="white",
        linewidth=0,
    )


def dev_progress(plan: dict[str, Any]) -> None:
    """A dev iterációk pontossága módszerenként (a „fejlődés” ábra)."""
    rows = []
    for step, item in enumerate(plan["dev"], start=1):
        for r in summary_rows(item["exp"], "dev"):
            rows.append({"step": step, "exp": item["exp"], "label": item["label"], **r})
    write_csv("dev_progress", rows)
    if not rows:
        return
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    for method, model in _keys(rows):
        pts = [r for r in rows if r["method"] == method and r["model"] == model]
        shift = {"M1": -0.06, "M2": 0.0, "M3": 0.06}[method]  # egybeeső pontok szétválasztása
        xs = [int(p["step"]) + shift for p in pts]
        ys = [float(p["accuracy"]) for p in pts]
        dash = "-" if model == "glm" else "--"
        ax.plot(xs, ys, dash, color=METHOD_COLORS[method], linewidth=2, marker="o", markersize=6)
        label = f"{method} {MODEL_NAMES[model]}"
        lift = {"M1": 7, "M2": 0, "M3": -7}[method]
        ax.annotate(label, (xs[-1], ys[-1]), xytext=(8, lift), textcoords="offset points",
                    va="center", fontsize=8, color=TEXT)  # fmt: skip
    ax.set_xticks([i + 1 for i in range(len(plan["dev"]))])
    ax.set_xticklabels([f"{d['exp']}\n{d['label']}" for d in plan["dev"]], fontsize=7)
    ax.set_xlim(0.7, len(plan["dev"]) + 1.2)
    ax.set_ylim(0, 1.05)
    style(ax, "pontosság a dev halmazon (20 kérdés)")
    ax.set_title("Fejlesztési iterációk a kis üzemen", fontsize=10)
    save(fig, "dev_progress")


def test_by_family(exp: str, split: str, name: str, title: str) -> None:
    """Egy mérés pontossága családonként, módszer × modell oszlopokkal."""
    rows = [r for fam in FAMILY_NAMES for r in summary_rows(exp, split, fam)]
    write_csv(name, rows)
    if not rows:
        return
    keys = _keys(rows)
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    width = 0.8 / len(keys)
    index = {(r["method"], r["model"], r["family"]): float(r["accuracy"]) for r in rows}
    for i, (method, model) in enumerate(keys):
        for j, fam in enumerate(FAMILY_NAMES):
            value = index.get((method, model, fam))
            if value is None:
                continue
            x = j + (i - (len(keys) - 1) / 2) * width
            _bar(ax, x, value, width * 0.92, method, model)
            ax.text(x, value + 0.01, f"{value:.2f}", ha="center", fontsize=6, color=TEXT)
    ax.set_xticks(range(len(FAMILY_NAMES)))
    ax.set_xticklabels(list(FAMILY_NAMES.values()), fontsize=8)
    ax.set_ylim(0, 1.1)
    handles = [
        Rectangle((0, 0), 1, 1, facecolor=METHOD_COLORS[m], hatch=MODEL_HATCH[mo]) for m, mo in keys
    ]
    labels = [f"{m} · {MODEL_NAMES[mo]}" for m, mo in keys]
    ax.legend(handles, labels, fontsize=7, ncol=3, frameon=False, loc="upper center",
              bbox_to_anchor=(0.5, -0.12))  # fmt: skip
    style(ax, "pontosság (helyes / összes)")
    ax.set_title(title, fontsize=10)
    save(fig, name)


def test_cost_latency(exp: str, split: str, name: str, title: str) -> None:
    """Két külön panel (nincs kettős tengely): kérdésenkénti költség és medián késleltetés."""
    data: list[dict[str, Any]] = [
        {
            "method": r["method"],
            "model": r["model"],
            "cost_per_question_usd": round(float(r["cost_usd"]) / int(r["n"]), 6),
            "latency_median_s": float(r["latency_median_s"]),
            "accuracy": float(r["accuracy"]),
        }
        for r in summary_rows(exp, split)
    ]
    write_csv(name, data)
    if not data:
        return
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.4))
    panels = [("cost_per_question_usd", "költség / kérdés (USD)", "{:.4f}"),
              ("latency_median_s", "medián késleltetés (s)", "{:.1f}")]  # fmt: skip
    for ax, (key, label, fmt) in zip(axes, panels, strict=True):
        for i, d in enumerate(data):
            _bar(ax, i, float(d[key]), 0.7, str(d["method"]), str(d["model"]))
            ax.text(i, float(d[key]), fmt.format(d[key]), ha="center", va="bottom", fontsize=7)
        ax.set_xticks(range(len(data)))
        ticks = [f"{d['method']}\n{MODEL_NAMES[str(d['model'])]}" for d in data]
        ax.set_xticklabels(ticks, fontsize=7)
        style(ax, label)
    fig.suptitle(f"{title} — {exp}", fontsize=10)
    save(fig, name)


def routes_figure(exp: str, name: str, title: str) -> None:
    """Az M1/M2 útvonalai (melyik tier vagy eszköz kellett a válaszhoz)."""
    path = RUNS / exp / "routes.csv"
    rows = [r for r in read_csv(path) if r["method"] in ("M1", "M2")] if path.exists() else []
    write_csv(name, rows)
    if not rows:
        return
    groups, routes = _keys(rows), sorted({r["route"] for r in rows})
    count = {(r["method"], r["model"], r["route"]): int(r["n"]) for r in rows}
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    for i, (method, model) in enumerate(groups):
        bottom = 0
        for k, route in enumerate(routes):
            n = count.get((method, model, route), 0)
            if not n:
                continue
            shade = ROUTE_SHADES[k % len(ROUTE_SHADES)]
            ax.bar(i, n, 0.6, bottom=bottom, color=shade, edgecolor="white", linewidth=2)
            ax.text(i, bottom + n / 2, str(n), ha="center", va="center", fontsize=7, color="white")
            bottom += n
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([f"{m}\n{MODEL_NAMES[mo]}" for m, mo in groups], fontsize=8)
    shades = [ROUTE_SHADES[k % len(ROUTE_SHADES)] for k in range(len(routes))]
    handles = [Rectangle((0, 0), 1, 1, color=s) for s in shades]
    ax.legend(handles, routes, fontsize=7, frameon=False, loc="center left",
              bbox_to_anchor=(1, 0.5))  # fmt: skip
    style(ax, "kérdések száma")
    ax.set_title(title, fontsize=10)
    save(fig, name)


def graph_layers(plan: dict[str, Any]) -> None:
    """Az összevont gráf csúcsai rétegenként és dokumentumonként (betöltési jelentés)."""
    report = json.loads((ROOT / "data/plant/load_report.json").read_text(encoding="utf-8"))
    counts = report["counts"]
    rows = [{"layer": "plant (PQA)", "nodes": counts["plant_nodes"]}]
    rows += [{"layer": d["doc"], "nodes": d["nodes"]} for d in counts["per_document"]]
    rows.append({"layer": "shared vocabulary", "nodes": counts["shared_vocabulary_nodes"]})
    write_csv("graph_layers", rows)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ys = list(range(len(rows)))
    ax.barh(ys, [int(r["nodes"]) for r in rows], 0.6, color="#2a78d6")
    for y, r in zip(ys, rows, strict=True):
        ax.text(int(r["nodes"]), y, f" {r['nodes']}", va="center", fontsize=7, color=TEXT)
    ax.set_yticks(ys)
    ax.set_yticklabels([str(r["layer"]) for r in rows], fontsize=7)
    ax.invert_yaxis()
    style(ax, "")
    ax.set_xlabel("csúcsok száma", color=MUTED)
    ax.set_title("Az összevont gráf rétegei", fontsize=10)
    save(fig, "graph_layers")


def pid_sheet() -> None:
    """A P&ID első lapja a rajzexport PDF-jéből (Benedek `demo.drawing`, EXP-003)."""
    import pymupdf

    doc: Any = pymupdf.open(ROOT / "data/plant/drawings/PQA/drawings.pdf")  # type: ignore[no-untyped-call]
    doc[0].get_pixmap(dpi=170).save(str(FIGURES / "pid_sheet0.png"))
    write_csv("pid_sheet0", [{"source": "data/plant/drawings/PQA/drawings.pdf", "page": 1}])


def _box(ax: Any, x: float, y: float, text: str, color: str, w: float = 2.6) -> None:
    ax.add_patch(Rectangle((x - w / 2, y - 0.32), w, 0.64, facecolor=color, edgecolor="none"))
    ax.text(x, y, text, ha="center", va="center", fontsize=7, color="white")


def _arrow(ax: Any, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": MUTED})


def methods_overview() -> None:
    """A három módszer sematikus felépítése (adat nélküli ábra)."""
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    columns = {
        "M1": ["kérdés", "Cypher-szint\n(üzem + adatlap séma)", "ágens + datasheet_fact",
               "összevont Neo4j-gráf"],
        "M2": ["kérdés", "router-ágens", "drawing: cascade_v4_iso\ndatasheet: plantdocs A2",
               "összevont Neo4j-gráf"],
        "M3": ["kérdés", "egy LLM-hívás", "egész rajz (ContextRAG)\n+ 12 adatlap-darab",
               "PDF-szöveg + vektorok"],
    }  # fmt: skip
    for i, (method, labels) in enumerate(columns.items()):
        x = 1.6 + i * 3.4
        ax.text(x, 4.05, method, ha="center", fontsize=10, fontweight="bold", color=TEXT)
        for k, label in enumerate(labels):
            _box(ax, x, 3.3 - k * 0.95, label, METHOD_COLORS[method] if k else MUTED)
            if k:
                _arrow(ax, (x, 3.3 - (k - 1) * 0.95 - 0.33), (x, 3.3 - k * 0.95 + 0.33))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 4.4)
    ax.axis("off")
    write_csv(
        "methods_overview", [{"method": m, "steps": " -> ".join(v)} for m, v in columns.items()]
    )
    save(fig, "methods_overview")


def main() -> None:
    """Minden ábra újragenerálása."""
    FIGURES.mkdir(exist_ok=True)
    plan = json.loads((FIGURES / "plan.json").read_text(encoding="utf-8"))
    pid_sheet()
    methods_overview()
    graph_layers(plan)
    dev_progress(plan)
    small = plan["test"]
    test_by_family(small, "test", "test_by_family", "Kis üzem, teszt (40 kérdés, családonként 10)")
    test_cost_latency(small, "test", "test_cost_latency", "Kis üzem: költség és késleltetés")
    routes_figure(small, "test_routes", "Útvonalak a kis üzem tesztjén")
    for item in plan["large"]:
        exp, name, label = item["exp"], item["name"], item["label"]
        test_by_family(exp, "dev+test", f"{name}_by_family", f"{label}, 60 kérdés, családonként 15")
        test_cost_latency(
            exp, "dev+test", f"{name}_cost_latency", f"{label}: költség és késleltetés"
        )
        routes_figure(exp, f"{name}_routes", f"Útvonalak, {label}")
    print(f"figures written to {FIGURES}")


if __name__ == "__main__":
    main()
