"""Melyik eszközgráf (TTL) melyik fájlból jön, és hol a Neo4j-kapcsolat beállítása."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from plantgraph.store.neo4j_settings import Neo4jSettings
from pydantic import SecretStr

ROOT = Path(__file__).resolve().parents[3]
PLANTDOCS = ROOT.parent / "plantdocs"
DATASHEETS = ROOT / "data" / "datasheets"

#: Az EXP-0030 Opus-gráfjai a plantdocs-ban (a felhasználó kérése: a meglévőknél az Opus-változat).
OPUS_GRAPHS_IN_PLANTDOCS = (
    "fisher-et-d100022x012",
    "gfps-165-solenoid-valve",
    "gorman-rupp-0700286",
)


def graph_path(document_id: str) -> Path:
    """Az eszköz TTL-gráfja: plantdocs `data/graphs/` vagy a saját Opus-feldolgozásunk."""
    if document_id in OPUS_GRAPHS_IN_PLANTDOCS:
        return PLANTDOCS / "data" / "graphs" / f"{document_id}.ttl"
    return DATASHEETS / document_id / "10-rdf" / "graph.ttl"


def pdf_path(document_id: str) -> Path:
    """Az eszköz adatlap-PDF-je (a demó és a forrásoldalak megjelenítéséhez)."""
    own = ROOT / "data" / "raw" / document_id / f"{document_id}.pdf"
    return own if own.exists() else PLANTDOCS / "data" / "raw" / f"{document_id}.pdf"


def neo4j_settings() -> Neo4jSettings:
    """A kapcsolat a plantqa `.env`-jéből (plantgraph-névvel: NEO4J_USERNAME)."""
    load_dotenv(ROOT / ".env", override=False)
    return Neo4jSettings(
        uri=os.environ["NEO4J_URI"],
        username=os.environ.get("NEO4J_USERNAME") or os.environ["NEO4J_USER"],
        password=SecretStr(os.environ["NEO4J_PASSWORD"]),
        database=os.environ.get("NEO4J_DATABASE", "neo4j"),
    )
