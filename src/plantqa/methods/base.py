"""A módszerek közös bemenete és kimenete."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol

from plantgraph.qa.final_answer import _answer_format_instruction
from plantgraph.qa.models import AnswerType


@dataclass(frozen=True)
class Question:
    """Amit egy módszer egy kérdésből lát: azonosító, szöveg, válaszalak, útválasztási címke."""

    qid: str
    text: str
    answer_type: str = "FREE_TEXT"
    label: str | None = None


@dataclass
class MethodAnswer:
    """Egy módszer válasza: a végső válasz (`{"answer", "not_present"}`) és a nyomai."""

    method: str
    model: str
    final: dict[str, Any] | None
    outcome: str
    route: list[str] = field(default_factory=list)
    cypher: list[str] = field(default_factory=list)
    sources: list[dict[str, Any]] = field(default_factory=list)
    latency_s: float = 0.0
    usage: dict[str, Any] = field(default_factory=dict)
    trace: Any = None

    def as_dict(self) -> dict[str, Any]:
        """JSON-ba írható alak."""
        return asdict(self)

    def text(self) -> str:
        """A válasz olvasható szövege (lista esetén vesszővel)."""
        if not self.final:
            return ""
        if self.final.get("not_present"):
            return "Not in the documents."
        value = self.final.get("answer")
        return ", ".join(map(str, value)) if isinstance(value, list) else str(value)


class Method(Protocol):
    """Egy kérdés-válaszoló módszer."""

    name: str

    def ask(self, question: Question) -> MethodAnswer:
        """Egy kérdés megválaszolása."""
        ...


def format_instruction(answer_type: str) -> str:
    """Benedek válaszalak-mondata (ugyanaz a szöveg, amit a cascade végső válasza lát)."""
    return _answer_format_instruction(AnswerType(answer_type))


def parse_final(text: str) -> dict[str, Any] | None:
    """Egy `{"answer": ..., "not_present": ...}` JSON-objektum a válasz szövegéből."""
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict) or "answer" not in data:
        return None
    return {"answer": data.get("answer"), "not_present": bool(data.get("not_present", False))}
