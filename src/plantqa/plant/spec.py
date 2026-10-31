"""A példaüzem rögzített beállításai és az elfogadási feltételek.

A generátor Benedek v1 generátora változtatás nélkül; a szűkítés két eszközzel történik:
a berendezéssúlyok csak adatlappal rendelkező osztályokat engednek, a szabályozókörök
változóját (F/L/P/T) pedig seedkereséssel szűrjük (csak F és P, mert a Rosemount 3051
nyomás- és különbségnyomásos áramlástávadó).

Két üzemprofil van, a `PLANTQA_PLANT` környezeti változó választ közöttük: `pqa` (alapértelmezés,
a négylapos példaüzem, EXP-002..EXP-040) és `pqb` (a nagyobb, kb. 30 lapos üzem ugyanazzal a
generátorral és ugyanazzal a hét adatlappal). A profil adja a korpusz azonosítóját, a
generátor méretét, az elfogadási határokat és a profil adat- és kérdésmappáját.
"""

from __future__ import annotations

import os
from pathlib import Path

from plantgraph.benchmark.generator_models import GeneratorConfig
from plantgraph.benchmark.split_models import ConnectorLabelDetail, SplitConfig

ROOT = Path(__file__).resolve().parents[3]
PROFILE = os.environ.get("PLANTQA_PLANT", "pqa").lower()
if PROFILE not in {"pqa", "pqb"}:
    raise ValueError(f"unknown plant profile {PROFILE!r} (PLANTQA_PLANT must be pqa or pqb)")
PLANT_ID = PROFILE
CORPUS_ID = PROFILE.upper()
N_UNITS = 2 if PROFILE == "pqa" else 15
EQUIPMENT_WEIGHTS = {"CentrifugalPump": 2.0, "HeatExchanger": 1.0}
#: A kis üzemen csak F és P kör lehet (seedszűrés); a nagyon az L és T kör is megmarad.
ALLOWED_LOOP_VARIABLES = frozenset({"F", "P"} if PROFILE == "pqa" else {"F", "L", "P", "T"})
MIN_TAGGED, MAX_TAGGED = (20, 40) if PROFILE == "pqa" else (120, 400)
MIN_SHEETS, MAX_SHEETS = (2, 4) if PROFILE == "pqa" else (24, 40)
#: A profil mappái: a kis üzemé a korábbi helyen marad, hogy a meglévő mérések érintetlenek.
PLANT_DIR = ROOT / "data" / ("plant" if PROFILE == "pqa" else "plant-pqb")
QUESTIONS_DIR = ROOT / "data" / ("questions" if PROFILE == "pqa" else "questions-pqb")
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
