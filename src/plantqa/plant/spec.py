"""A példaüzem rögzített beállításai és az elfogadási feltételek.

A generátor Benedek v1 generátora változtatás nélkül; a szűkítés két eszközzel történik:
a berendezéssúlyok csak adatlappal rendelkező osztályokat engednek, a szabályozókörök
változóját (F/L/P/T) pedig seedkereséssel szűrjük (csak F és P, mert a Rosemount 3051
nyomás- és különbségnyomásos áramlástávadó).
"""

from __future__ import annotations

from plantgraph.benchmark.generator_models import GeneratorConfig
from plantgraph.benchmark.split_models import ConnectorLabelDetail, SplitConfig

PLANT_ID = "pqa"
CORPUS_ID = "PQA"
N_UNITS = 2
EQUIPMENT_WEIGHTS = {"CentrifugalPump": 2.0, "HeatExchanger": 1.0}
ALLOWED_LOOP_VARIABLES = frozenset({"F", "P"})
MIN_TAGGED, MAX_TAGGED = 20, 40
MIN_SHEETS, MAX_SHEETS = 2, 4
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
