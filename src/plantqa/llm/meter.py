"""Kérdésenkénti mérő: tokenek, költség (cache-ből is a rögzített ár), valódi költés, hívásszám.

Egy folyamatban egy aktív mérő van (`current()`); a futtató kérdésenként újat indít. A két
kliens (`clients.py`) minden hívásnál ide is ír.
"""

from __future__ import annotations

import threading
from dataclasses import asdict, dataclass, field
from typing import Any

_LOCK = threading.Lock()


@dataclass
class Meter:
    """Egy kérdés összesített LLM-használata."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0
    spent_usd: float = 0.0
    n_calls: int = 0
    n_cached: int = 0
    models: set[str] = field(default_factory=set)

    def add(self, model: str, prompt: int, completion: int, cost: float, cached: bool) -> None:
        """Egy hívás hozzáadása; `cost` a szolgáltató által jelentett ár (cache-nél az eredeti)."""
        with _LOCK:
            self.prompt_tokens += prompt
            self.completion_tokens += completion
            self.cost_usd += cost
            self.spent_usd += 0.0 if cached else cost
            self.n_calls += 1
            self.n_cached += int(cached)
            self.models.add(model)

    def as_dict(self) -> dict[str, Any]:
        """JSON-ba írható alak."""
        data = asdict(self)
        data["models"] = sorted(self.models)
        return data


_ACTIVE = Meter()


def current() -> Meter:
    """Az aktív mérő."""
    return _ACTIVE


def start() -> Meter:
    """Új mérő indítása (kérdésenként)."""
    global _ACTIVE
    _ACTIVE = Meter()
    return _ACTIVE
