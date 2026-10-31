from __future__ import annotations

import networkx as nx

from plantqa.plant import datasheets
from plantqa.plant.search import loop_variables, try_seed


def _plant() -> nx.DiGraph[str]:
    g: nx.DiGraph[str] = nx.DiGraph()
    g.add_node("v1", node_class="GlobeValve", tag="FV-1-1")
    g.add_node("v2", node_class="GlobeValve", tag="GV-1-1")
    g.add_node("p", node_class="CentrifugalPump", tag="P-1-1")
    g.add_node("c", node_class="ProcessInstrumentationFunction", tag="FIC-1-1")
    g.add_node("a", node_class="ActuatingFunction")
    g.add_edge("a", "v1", relation="control")
    return g


def test_globe_valve_role_decides_datasheet() -> None:
    mapping = datasheets.tag_to_datasheet(_plant())
    assert mapping["FV-1-1"] == datasheets.CONTROL_VALVE
    assert mapping["GV-1-1"] == datasheets.SOLENOID_VALVE
    assert mapping["P-1-1"] == datasheets.PUMP


def test_controller_has_no_datasheet_but_a_reason() -> None:
    rows = {r["tag"]: r for r in datasheets.tag_rows(_plant())}
    assert rows["FIC-1-1"]["document_id"] is None
    assert "DCS" in rows["FIC-1-1"]["no_datasheet_reason"]
    assert len(rows) == 4


def test_accepted_seed_is_reproducible() -> None:
    first, second = try_seed(6), try_seed(6)
    assert first.failures == []
    assert nx.utils.graphs_equal(first.corpus.plant, second.corpus.plant)
    assert loop_variables(first.corpus.plant) <= {"F", "P"}
