"""A tudásgráf-építés két sematikus ábrája (adat nélküli): `python -m plantqa.figures_kg`.

`kg_pipeline`: a két forrásfolyamat és az összekötés lépései egy folyamatábrán.
`kg_example`: az összevont gráf egy szemléltető részlete (egy szivattyú a rajzon, az adatlapja
és egy feltételes adatpont). A színek a módszerábráéval egyeznek.
"""

from __future__ import annotations

from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from plantqa.figures import FIGURES, MUTED, TEXT, save  # noqa: E402

DRAWING = "#2a78d6"
DATASHEET = "#1a8f63"
LINK = "#eb6834"
MERGED = "#3b3a37"
ROUND = "round,pad=0,rounding_size=0.08"


def _box(ax: Any, x: float, y: float, text: str, color: str, w: float, h: float = 0.78) -> None:
    shape = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=ROUND, facecolor=color,
                           edgecolor="none")  # fmt: skip
    ax.add_patch(shape)
    ax.text(x, y, text, ha="center", va="center", fontsize=6.6, color="white", linespacing=1.25)


def _arrow(ax: Any, start: tuple[float, float], end: tuple[float, float], label: str = "") -> None:
    style = {"arrowstyle": "-|>", "color": MUTED, "lw": 0.9, "shrinkA": 0, "shrinkB": 0}
    ax.annotate("", xy=end, xytext=start, arrowprops=style)
    if label:
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(mx, my, label, ha="center", va="center", fontsize=6, color=TEXT,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.2})  # fmt: skip


def _row(ax: Any, y: float, xs: list[float], labels: list[str], color: str, w: float) -> None:
    for k, (x, label) in enumerate(zip(xs, labels, strict=True)):
        _box(ax, x, y, label, color, w)
        if k:
            _arrow(ax, (xs[k - 1] + w / 2, y), (x - w / 2, y))


def kg_pipeline() -> None:
    """A tudásgráf felépítése: rajzi és adatlapi folyamat, összekötés, közös adatbázis."""
    fig, ax = plt.subplots(figsize=(7.3, 3.3))
    top, mid, bottom = 3.3, 1.95, 0.6
    lanes = [(top, "rajzok", DRAWING), (mid, "összekötés", LINK), (bottom, "adatlapok", DATASHEET)]
    for y, name, color in lanes:
        ax.text(0.3, y, name, ha="center", va="center", fontsize=7.5, fontweight="bold",
                color=color, rotation=90)  # fmt: skip
    w = 1.95
    xs = [1.65, 3.8, 5.95, 8.1]
    _row(ax, top, xs, [
        "1. üzem generálása\nszabályok szerint",
        "2. lapokra bontás\nlapközi csatlakozókkal",
        "3. visszaépítés a lapokból\n(csatlakozópárok,\nazonos elemek)",
        "4. üzemi réteg\nbetöltése",
    ], DRAWING, w)  # fmt: skip
    _row(ax, bottom, xs, [
        "1. PDF elrendezés-\nelemzése",
        "2. értékek, táblázatok,\nábrák kinyerése,\nellenőrzés a PDF-fel",
        "3. tények feltételekkel,\nszabványos fogalmakkal\n→ RDF-gráf",
        "4. adatlapgráfok\nbetöltése",
    ], DATASHEET, w)  # fmt: skip
    _row(ax, mid, xs[1:], [
        "tag → adatlap tábla\n(az elemek osztályából)",
        "összekötő élek:\nrajzi elem → adatlap",
        "vektorindex\naz adatpontokra",
    ], LINK, w)  # fmt: skip
    _box(ax, 10.35, mid, "összevont\ntudásgráf\n(egy Neo4j-\nadatbázis)", MERGED, 1.3, 3.4)
    for y in (top, mid, bottom):
        _arrow(ax, (xs[-1] + w / 2, y), (10.35 - 0.65, y))
    ax.set_xlim(0, 11.05)
    ax.set_ylim(0, 3.95)
    ax.axis("off")
    save(fig, "kg_pipeline")


def kg_example() -> None:
    """Az összevont gráf szemléltető részlete: rajzi réteg, összekötő él, adatlapi réteg."""
    fig, ax = plt.subplots(figsize=(6.8, 3.5))
    ax.add_patch(FancyBboxPatch((0.1, 2.55), 10.4, 2.0, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor="#eaf2fc", edgecolor="none"))  # fmt: skip
    ax.add_patch(FancyBboxPatch((0.1, -0.2), 10.4, 2.6, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor="#e8f5ef", edgecolor="none"))  # fmt: skip
    ax.text(0.25, 4.35, "rajzi réteg", fontsize=8, fontweight="bold", color=DRAWING, va="center")
    ax.text(
        0.25, 2.28, "adatlapi réteg", fontsize=8, fontweight="bold", color=DATASHEET, va="center"
    )
    w = 2.0
    _box(ax, 1.6, 3.3, "CHV-1-2\nvisszacsapó szelep", DRAWING, w)
    _box(ax, 4.6, 3.3, "P-1-3\ncentrifugálszivattyú", DRAWING, w)
    _box(ax, 7.6, 3.3, "P-2-1\ncentrifugálszivattyú", DRAWING, w)
    _box(ax, 9.3, 4.15, "rajzlap", DRAWING, 1.2, 0.5)
    _arrow(ax, (1.6 + w / 2, 3.3), (4.6 - w / 2, 3.3), "áramlás")
    _arrow(ax, (4.6 + w / 2, 3.3), (7.6 - w / 2, 3.3), "áramlás")
    _arrow(ax, (5.3, 3.69), (8.7, 4.15), "szerepel rajta")
    _box(ax, 4.6, 1.75, "Gorman-Rupp VGH\nszivattyú (az adatlap\ngyökércsúcsa)", DATASHEET, w)
    _arrow(ax, (4.6, 3.3 - 0.39), (4.6, 1.75 + 0.39), "összekötő él (tag alapján)")
    _box(ax, 4.6, 0.45, "adatpont: legnagyobb\nüzemi nyomás\n250 psi", DATASHEET, w)
    _arrow(ax, (4.6, 0.45 + 0.39), (4.6, 1.75 - 0.39), "alanya")
    _box(ax, 1.6, 0.45, "eset: a feltételek\negyüttese", DATASHEET, w)
    _arrow(ax, (4.6 - w / 2, 0.45), (1.6 + w / 2, 0.45), "érvényes")
    _box(ax, 1.6, 1.75, "feltétel: hőmérséklet\nlegfeljebb 100 °F", DATASHEET, w)
    _arrow(ax, (1.6, 1.75 - 0.39), (1.6, 0.45 + 0.39), "része")
    _box(ax, 8.3, 0.45, "mértékegység: psi\n(QUDT-megfeleltetéssel)", DATASHEET, 2.3)
    _arrow(ax, (4.6 + w / 2, 0.45), (8.3 - 1.15, 0.45), "mértékegysége")
    _box(ax, 8.3, 1.75, "forrás: táblázat\nés PDF-oldal", DATASHEET, 2.3)
    _arrow(ax, (4.6 + w / 2, 0.75), (8.3 - 1.15, 1.45), "forrása")
    ax.set_xlim(0, 10.6)
    ax.set_ylim(-0.3, 4.65)
    ax.axis("off")
    save(fig, "kg_example")


def main() -> None:
    """A két sematikus ábra újragenerálása."""
    FIGURES.mkdir(exist_ok=True)
    kg_pipeline()
    kg_example()


if __name__ == "__main__":
    main()
