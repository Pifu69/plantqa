"""Adatlapi kérdés egy eszközről a plantdocs A2 logikájával, az összevont gráfon.

Ugyanaz a hívás, mint a plantdocs appban (`app/engine.py`): `ask_graph(client, "A2", …)`
leltárral, szakaszkatalógussal és vektoros kereséssel. Különbség az összevont gráf miatt:
a lekérdezés-futtató csak olyan lekérdezést enged, amely a dokumentumra szűkít (a csúcsok
`document_id` tulajdonsága vagy az URI-előtag), és ezt a leltár elé írt sor kéri; a vektoros
keresés találatai közül csak a dokumentuméi maradnak.
"""

from __future__ import annotations

import re
from typing import Any

from neo4j import Driver
from plantdocs.graph.vectors import similar_block
from plantdocs.llm.embeddings import Embedder
from plantdocs.llm.openrouter import Client
from plantdocs.qa.context import inventory
from plantdocs.qa.run import WRITES, Executor, ask_graph
from plantdocs.qa.sections import Catalog, catalog
from rdflib import Graph

from plantqa.graph.load import open_driver
from plantqa.graph.sources import graph_path
from plantqa.llm.clients import CACHE_DIR, plantdocs_chat_transport, plantdocs_embed_transport
from plantqa.llm.pins import ModelKey, pin, plantdocs_settings

MAX_CELL = 300
VECTOR_POOL = 600
TOP_K = 30
SCOPE = (
    "SCOPE: this Neo4j database holds the datasheet graphs of several devices. This question is "
    "about document '{doc}' only. Every node of this document has the property "
    "document_id = '{doc}' (and its uri starts with 'urn:plantdocs:{doc}:'). Restrict every "
    "MATCH to it, e.g. WHERE d.document_id = '{doc}'; a query without this filter is refused.\n\n"
)
NEAREST = """CALL db.index.vector.queryNodes('plantdocs_vectors', $k, $v) YIELD node AS d, score
WITH d, score WHERE d.document_id = $doc
OPTIONAL MATCH (d)-[:plm__PCA_100029525]->(s)
OPTIONAL MATCH (d)-[:plm__PCA_100029520]->(c)
OPTIONAL MATCH (d)-[:plm__PCA_100029514]->(f)
WITH d, s, c, score, collect(DISTINCT f.plm__PCA_100029522) AS notes
RETURN d.plm__PCA_100029521 AS label, d.plm__PCA_100029522 AS value,
  c.rdfs__label AS conditions,
  reduce(t = "", x IN notes | t + CASE WHEN t = "" THEN "" ELSE " / " END + x) AS footnote,
  d.schema__pageStart AS page, s.plm__PCA_100029521 AS section,
  d.dct__type AS kind, d.dct__description AS description, score
ORDER BY score DESC LIMIT $top"""

Loaded = tuple[Graph, str, Catalog]


def _text(value: Any) -> str:
    return "" if value is None else str(value)[:MAX_CELL]


def scoped_executor(driver: Driver, document_id: str) -> Executor:
    """Csak olvasó, a dokumentumra szűkítő Cypher-futtató (a plantdocs futtatójának mintájára)."""

    def run(query: str) -> list[dict[str, Any]]:
        if WRITES.search(query):
            raise ValueError("only read queries are allowed")
        if not re.search(re.escape(document_id), query):
            raise ValueError(f"the query must restrict to document_id = '{document_id}'")
        records, _, _ = driver.execute_query(query, routing_="r")
        return [{k: _text(r[k]) for k in r.keys()} for r in records]

    return run


class DatasheetQA:
    """A2-kérdezés eszközönként; gráfok, leltárak, katalógusok egyszer betöltve."""

    def __init__(self, model: ModelKey, allow_paid: bool, driver: Driver | None = None) -> None:
        """A plantdocs kliense a modell pinjével, a cache-elt szállítóval."""
        transport = plantdocs_chat_transport(allow_paid)
        self.model = model
        self.client = Client(
            CACHE_DIR / "plantdocs-calls.jsonl",
            transport,
            model=pin(model).model_id,
            settings=plantdocs_settings(model),
        )
        self.embedder = Embedder(CACHE_DIR / "plantdocs-embed-calls.jsonl")
        self.embedder.transport = plantdocs_embed_transport(allow_paid)
        self.driver = driver or open_driver()
        self._graphs: dict[str, Loaded] = {}

    def _graph(self, document_id: str) -> Loaded:
        if document_id not in self._graphs:
            graph = Graph().parse(graph_path(document_id))
            self._graphs[document_id] = (graph, inventory(graph), catalog(graph))
        return self._graphs[document_id]

    def _similar(self, document_id: str, question: str) -> tuple[str, int]:
        vector = self.embedder.embed([question], tag=f"plantqa/A2/{document_id}")[0]
        records, _, _ = self.driver.execute_query(
            NEAREST, k=VECTOR_POOL, v=vector, doc=document_id, top=TOP_K, routing_="r"
        )
        found = [dict(r) for r in records]
        return similar_block(found), len(found)

    def ask(self, document_id: str, question: str, qid: str = "plantqa") -> dict[str, Any]:
        """Egy kérdés egy dokumentumról; a plantdocs eredménye a dokumentum azonosítójával."""
        _, context, sections = self._graph(document_id)
        scoped = SCOPE.format(doc=document_id) + context
        result = ask_graph(
            self.client,
            "A2",
            {"id": qid, "question": question},
            scoped,
            scoped_executor(self.driver, document_id),
            None,
            sections,
            lambda q: self._similar(document_id, q),
        )
        return {**result, "document_id": document_id}
