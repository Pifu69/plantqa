"""Az összetett kérdések topológiai lépései a gold üzemgráfból (program, nem LLM).

Egy lépés: kiinduló tag + reláció → pontosan egy cél-tag. Csak egyértelmű lépést tartunk meg,
és csak olyat, amelynek cél-tagjéhez van plantdocs gold kérdés (a `document_id` szerint).
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

import networkx as nx

from plantqa.plant.datasheets import controlled_valves, datasheet_for

PHRASES = {
    "measured_by": "the transmitter that measures {anchor}",
    "operated_by": "the valve operated by control loop {anchor}",
    "fed_by_transmitter": "the transmitter that feeds controller {anchor}",
    "downstream": "the item directly downstream of {anchor} in the process flow",
    "upstream": "the item directly upstream of {anchor} in the process flow",
}


@dataclass(frozen=True)
class Step:
    """Egy egyértelmű topológiai lépés: `anchor` --reláció--> `target` (tagekkel)."""

    relation: str
    anchor: str
    target: str
    target_document: str

    @property
    def phrase(self) -> str:
        """A lépés angol megfogalmazása a kérdésben."""
        return PHRASES[self.relation].format(anchor=self.anchor)


def _tag(plant: nx.DiGraph[str], node: str) -> str | None:
    tag = plant.nodes[node].get("tag")
    return str(tag) if tag else None


def _edges(plant: nx.DiGraph[str], relation: str) -> list[tuple[str, str]]:
    return [(a, b) for a, b, d in plant.edges(data=True) if d.get("relation") == relation]


def _signal_chain(plant: nx.DiGraph[str]) -> Iterator[tuple[str, str, str]]:
    """(távadó, szabályozó, szelep) hármasok a jel- és működtetési éleken át."""
    signal = dict(_edges(plant, "send_signal_to"))
    control = dict(_edges(plant, "control"))
    for transmitter, controller in signal.items():
        actuator = signal.get(controller)
        if actuator in control:
            yield transmitter, controller, control[actuator]


def _raw_steps(plant: nx.DiGraph[str]) -> Iterator[tuple[str, str, str]]:
    """(reláció, kiinduló csúcs, cél csúcs) — egyértelműség-ellenőrzés nélkül."""
    for equipment, transmitter in _edges(plant, "measured_by"):
        yield "measured_by", equipment, transmitter
    for transmitter, controller, valve in _signal_chain(plant):
        yield "operated_by", controller, valve
        yield "fed_by_transmitter", controller, transmitter
    flow = nx.DiGraph(_edges(plant, "send_to"))
    for node in flow.nodes:
        successors, predecessors = list(flow.successors(node)), list(flow.predecessors(node))
        if len(successors) == 1:
            yield "downstream", node, successors[0]
        if len(predecessors) == 1:
            yield "upstream", node, predecessors[0]


def steps(plant: nx.DiGraph[str], with_gold: set[str]) -> list[Step]:
    """Az egyértelmű lépések, amelyek cél-tagjének adatlapjához van gold kérdés."""
    controlled = controlled_valves(plant)
    out = []
    for relation, src, dst in _raw_steps(plant):
        anchor, target = _tag(plant, src), _tag(plant, dst)
        document = datasheet_for(dst, dict(plant.nodes[dst]), controlled)
        if anchor and target and document in with_gold:
            out.append(Step(relation, anchor, target, str(document)))
    return sorted(out, key=lambda s: (s.relation, s.anchor))
