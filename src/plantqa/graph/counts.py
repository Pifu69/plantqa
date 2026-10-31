"""Csúcs- és élszámok rétegenként az összevont gráfban."""

from __future__ import annotations

from typing import Any

from neo4j import Driver

QUERIES = {
    "plant_nodes": "MATCH (n:CorpusNode {corpus_id: $c}) RETURN count(n) AS n",
    "plant_relationships": "MATCH (:CorpusNode {corpus_id: $c})-[r]->(:CorpusNode) "
    "RETURN count(r) AS n",
    "device_nodes": "MATCH (n:Resource) WHERE n.document_id IS NOT NULL RETURN count(n) AS n",
    "shared_vocabulary_nodes": "MATCH (n:Resource) WHERE n.document_id IS NULL "
    "RETURN count(n) AS n",
    "device_relationships": "MATCH (:Resource)-[r]->(:Resource) RETURN count(r) AS n",
    "described_by": "MATCH (:CorpusNode)-[r:DESCRIBED_BY]->(:Resource) RETURN count(r) AS n",
    "all_nodes": "MATCH (n) RETURN count(n) AS n",
    "all_relationships": "MATCH ()-[r]->() RETURN count(r) AS n",
}
PER_DOCUMENT = (
    "MATCH (n:Resource) WHERE n.document_id IS NOT NULL "
    "OPTIONAL MATCH (n)-[r]->(:Resource) "
    "RETURN n.document_id AS doc, count(DISTINCT n) AS nodes, count(r) AS relationships "
    "ORDER BY doc"
)


def layer_counts(driver: Driver, corpus_id: str) -> dict[str, Any]:
    """Az összes számláló és a dokumentumonkénti bontás."""
    out: dict[str, Any] = {}
    with driver.session() as session:
        for name, query in QUERIES.items():
            record = session.run(query, c=corpus_id).single()
            out[name] = int(record["n"]) if record else 0
        out["per_document"] = [dict(r) for r in session.run(PER_DOCUMENT)]
    return out
