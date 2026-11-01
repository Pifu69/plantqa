"""A példaüzem rögzített beállításai és az elfogadási feltételek.

A generátor Benedek v1 generátora változtatás nélkül; a szűkítés két eszközzel történik:
a berendezéssúlyok csak adatlappal rendelkező osztályokat engednek, a szabályozókörök
változóját (F/L/P/T) pedig seedkereséssel szűrjük (csak F és P, mert a Rosemount 3051
nyomás- és különbségnyomásos áramlástávadó).

Három üzemprofil van, a `PLANTQA_PLANT` környezeti változó választ közöttük: `pqa` (alapértelmezés,
a négylapos példaüzem, EXP-002..EXP-040), `pqb` (27 lap) és `pqc` (98 lap) a korábbi nagy üzemek,
`p30` és `p50` a pontosan 30 és 50 lapos fejlesztési üzemek, `p100` és `p1000` a pontosan 100 és
1000 lapos tesztüzemek (az egységszámot
úgy választottuk, hogy a lapszám pontosan elérhető legyen), mind ugyanazzal a generátorral és
ugyanazzal a hét adatlappal. A profil adja a korpusz azonosítóját, a
generátor méretét, az elfogadási határokat és a profil adat- és kérdésmappáját.
"""

from __future__ import annotations

import os
from pathlib import Path

from plantgraph.benchmark.generator_models import GeneratorConfig
from plantgraph.benchmark.split_models import ConnectorLabelDetail, SplitConfig

ROOT = Path(__file__).resolve().parents[3]
PROFILE = os.environ.get("PLANTQA_PLANT", "pqa").lower()
#: Profilonként: egységszám, a tagelt elemek és a lapok elfogadási határa.
PROFILES = {
    "pqa": (2, (20, 40), (2, 4)),
    "pqb": (15, (120, 400), (24, 40)),
    "pqc": (55, (500, 1500), (90, 115)),
    "p30": (17, (150, 300), (30, 30)),
    "p50": (28, (250, 600), (50, 50)),
    "p100": (57, (500, 1500), (100, 100)),
    "p1000": (600, (5000, 15000), (1000, 1000)),
}
if PROFILE not in PROFILES:
    raise ValueError(f"unknown plant profile {PROFILE!r} (PLANTQA_PLANT: {sorted(PROFILES)})")
PLANT_ID = PROFILE
CORPUS_ID = PROFILE.upper()
N_UNITS, (MIN_TAGGED, MAX_TAGGED), (MIN_SHEETS, MAX_SHEETS) = PROFILES[PROFILE]
EQUIPMENT_WEIGHTS = {"CentrifugalPump": 2.0, "HeatExchanger": 1.0}
#: A kis üzemen csak F és P kör lehet (seedszűrés); a nagyobbakon az L és T kör is megmarad.
ALLOWED_LOOP_VARIABLES = frozenset({"F", "P"} if PROFILE == "pqa" else {"F", "L", "P", "T"})
#: A profil mappái: a kis üzemé a korábbi helyen marad, hogy a meglévő mérések érintetlenek.
PLANT_DIR = ROOT / "data" / ("plant" if PROFILE == "pqa" else f"plant-{PROFILE}")
QUESTIONS_DIR = ROOT / "data" / ("questions" if PROFILE == "pqa" else f"questions-{PROFILE}")
SHEET_EQUIPMENT_BUDGET = 4


def generator_config(seed: int) -> GeneratorConfig:
    """A generátor beállításai egy adott seedre."""
    return GeneratorConfig(
        plant_id=PLANT_ID,
        seed=seed,
        n_units=N_UNITS,
        equipment_per_unit_min=4,
        equipment_per_unit_max=6,
        equipment_weights=EQUIPMENT_WEIGHTS,
        valves_per_stream_max=2,
        p_control_loop=0.7,
    )


def split_config(seed: int) -> SplitConfig:
    """A lapokra bontás beállításai: Benedek headline-presetje, kisebb laponkénti kerettel."""
    return SplitConfig(
        strategy="by_unit",
        sheet_equipment_budget=SHEET_EQUIPMENT_BUDGET,
        seed=seed,
        connector_label_detail=ConnectorLabelDetail.DRAWING_ONLY,
        duplication_rate=0.25,
        exact_match_tags=True,
    )
