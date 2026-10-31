"""Tag → plantdocs-adatlap hozzárendelés a generált üzem gráfjából (program állítja elő).

A szabály osztály és szerep szerint dönt: a szabályozókörbe kötött globe szelep a Fisher ET
szabályozószelep, a kör nélküli globe szelep a GF 165 mágnesszelep (kétutas, globe kialakítású
nyitó-záró szelep); a szabályozófunkciók (xIC) DCS-funkciók, gyártói adatlapjuk nincs. A
Rosemount 3051 nyomás- és különbségnyomásos távadó, ezért csak az F és P távadóhoz tartozik; a
nagy üzem szint- (LT) és hőmérséklet-távadójához (TT) nincs adatlap a gyűjteményben.
"""

from __future__ import annotations

from typing import Any

import networkx as nx

PUMP = "gorman-rupp-0700286"
CONTROL_VALVE = "fisher-et-d100022x012"
SOLENOID_VALVE = "gfps-165-solenoid-valve"
BALL_VALVE = "flowserve-worcester-f51-f52"
CHECK_VALVE = "swagelok-ms-01-176"
HEAT_EXCHANGER = "alfalaval-m3"
TRANSMITTER = "rosemount-3051-00813-0100-4001"

BY_CLASS = {
    "CentrifugalPump": PUMP,
    "HeatExchanger": HEAT_EXCHANGER,
    "BallValve": BALL_VALVE,
    "CheckValve": CHECK_VALVE,
    "ProcessSignalGeneratingFunction": TRANSMITTER,
}
#: A Rosemount 3051 által mérhető változók (a távadó tagjének első betűje).
TRANSMITTER_VARIABLES = frozenset({"F", "P"})
NO_DATASHEET = {
    "ProcessInstrumentationFunction": "control function in the DCS (shared display/control); "
    "no vendor datasheet exists for it",
    "ProcessSignalGeneratingFunction": "level or temperature transmitter; the corpus has no "
    "datasheet for it (the Rosemount 3051 measures pressure and differential-pressure flow)",
}


def controlled_valves(plant: nx.DiGraph[str]) -> set[str]:
    """A szabályozókör által működtetett szelepek csúcsazonosítói (`control` él végpontjai)."""
    return {dst for _, dst, data in plant.edges(data=True) if data.get("relation") == "control"}


def datasheet_for(node: str, data: dict[str, Any], controlled: set[str]) -> str | None:
    """Egy tagelt csúcs adatlapja; `None`, ha az osztályhoz nincs adatlap."""
    node_class = data.get("node_class", "")
    if node_class == "GlobeValve":
        return CONTROL_VALVE if node in controlled else SOLENOID_VALVE
    if node_class == "ProcessSignalGeneratingFunction":
        return TRANSMITTER if str(data.get("tag", ""))[:1] in TRANSMITTER_VARIABLES else None
    return BY_CLASS.get(node_class)


def tag_rows(plant: nx.DiGraph[str]) -> list[dict[str, Any]]:
    """Minden tagelt csúcs egy sora: tag, osztály, csúcs, adatlap (vagy indoklás)."""
    controlled = controlled_valves(plant)
    tagged = [(str(n), dict(d)) for n, d in plant.nodes(data=True) if d.get("tag")]
    rows = []
    for node, data in sorted(tagged, key=lambda item: str(item[1]["tag"])):
        row: dict[str, Any] = {
            "tag": data["tag"],
            "node_class": data["node_class"],
            "node_id": node,
        }
        row["document_id"] = datasheet_for(node, data, controlled)
        if row["document_id"] is None:
            row["no_datasheet_reason"] = NO_DATASHEET.get(data["node_class"], "unmapped class")
        rows.append(row)
    return rows


def tag_to_datasheet(plant: nx.DiGraph[str]) -> dict[str, str]:
    """Csak az adatlappal rendelkező tagek: tag → document_id."""
    return {row["tag"]: row["document_id"] for row in tag_rows(plant) if row["document_id"]}
