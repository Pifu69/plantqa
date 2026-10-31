"""A két QA-modell rögzített pinjei (Benedek pin-JSON-jai; a GLM „high” a `pin_low` másolata).

`luna_low.json` = Thesis `data/runs/exp0007/inputs/pin_cypher_luna_low.json`,
`luna_high.json` = `pin_agent_luna_final_high.json`, `glm_low.json` = `data/runs/cv1/pin_low.json`.
"""

from __future__ import annotations

import json
from typing import Literal

from plantgraph.llm.models import ModelPin

from plantqa.graph.sources import ROOT

ModelKey = Literal["glm", "luna"]
Effort = Literal["low", "high"]
MODEL_KEYS: tuple[ModelKey, ...] = ("glm", "luna")
PINS_DIR = ROOT / "pins"


def pin(model: ModelKey, effort: Effort = "low") -> ModelPin:
    """A modell pinje a megadott gondolkodási szinttel."""
    path = PINS_DIR / f"{model}_{effort}.json"
    return ModelPin.model_validate(json.loads(path.read_text(encoding="utf-8")))


def plantdocs_settings(model: ModelKey) -> dict[str, object]:
    """A plantdocs `Client` beállításai ugyanabból a pinből (a reasoning-et az A2 maga adja)."""
    p = pin(model, "low")
    settings: dict[str, object] = {"max_tokens": p.max_output_tokens}
    if p.temperature is not None:
        settings["temperature"] = p.temperature
    if p.seed is not None:
        settings["seed"] = p.seed
    if p.route_provider:
        settings["provider"] = {"order": [p.route_provider], "allow_fallbacks": False}
    return settings
