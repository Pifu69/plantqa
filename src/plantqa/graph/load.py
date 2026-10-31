"""Az összevont gráf betöltése egy paranccsal: `python -m plantqa.graph.load`.

Sorrend: (1) teljes törlés és n10s-beállítás (plantdocs `reset`), (2) minden szükséges
eszközgráf n10s-sel (a csúcsok `document_id` tulajdonságot kapnak — ez a névtér, az URI-k
már eleve `urn:plantdocs:<doc>:` kezdetűek), (3) Benedek üzemrétege a saját betöltőjével
(`plant_lines` profil; csak a saját korpuszát törli), (4) a `DESCRIBED_BY` élek tagenként.
A mérések (csúcs- és élszám rétegenként, idők) a `data/plant/load_report.json`-ba kerülnek.
"""

from __future__ import annotations

import json
import time
from typing import Any

from neo4j import Driver, GraphDatabase
from plantdocs.graph import neo4j_load
from plantgraph.qa.corpus import load_corpus_artifacts
from plantgraph.store.neo4j_loader import load_corpus

from plantqa.graph.counts import layer_counts
from plantqa.graph.sources import ROOT, graph_path, neo4j_settings
from plantqa.plant.spec import CORPUS_ID

PLANT_DIR = ROOT / "data" / "plant"
INGEST_JSON = PLANT_DIR / "corpora" / CORPUS_ID / "ingest.json"
REPORT = PLANT_DIR / "load_report.json"

TAG_NAMESPACE = (
    "MATCH (n:Resource) WHERE n.uri STARTS WITH $prefix SET n.document_id = $doc "
    "RETURN count(n) AS n"
)
LINK = (
    "UNWIND $rows AS row "
    "MATCH (p:CorpusNode:PlantItem {corpus_id: $corpus, tag: row.tag}) "
    "MATCH (d:Resource {uri: row.device}) "
    "MERGE (p)-[:DESCRIBED_BY]->(d) RETURN count(*) AS n"
)


def device_uri(document_id: str) -> str:
    """Az eszköz gyökércsúcsának URI-ja a plantdocs gráfjában."""
    return f"urn:plantdocs:{document_id}:device"


def open_driver() -> Driver:
    """Kapcsolat a beállított adatbázishoz."""
    s = neo4j_settings()
    return GraphDatabase.driver(s.uri, auth=(s.username, s.password.get_secret_value()))


def tag_mapping() -> dict[str, str]:
    """A program által előállított tag → document_id hozzárendelés."""
    path = PLANT_DIR / "tag_to_datasheet.json"
    return dict(json.loads(path.read_text(encoding="utf-8")))


def available(mapping: dict[str, str]) -> tuple[list[str], list[str]]:
    """A hozzárendelés dokumentumai: amelyeknek van gráfja, és amelyeknek (még) nincs."""
    documents = sorted(set(mapping.values()))
    present = [d for d in documents if graph_path(d).exists()]
    return present, [d for d in documents if d not in present]


def load_devices(driver: Driver, documents: list[str]) -> dict[str, Any]:
    """Az eszközgráfok betöltése n10s-sel; dokumentumonként idő és csúcsszám."""
    timings: dict[str, Any] = {}
    for doc in documents:
        start = time.perf_counter()
        neo4j_load.load(driver, graph_path(doc).read_text(encoding="utf-8"))
        with driver.session() as session:
            record = session.run(TAG_NAMESPACE, prefix=f"urn:plantdocs:{doc}:", doc=doc).single()
        nodes = int(record["n"]) if record else 0
        timings[doc] = {"seconds": time.perf_counter() - start, "nodes": nodes}
    return timings


def link_tags(driver: Driver, mapping: dict[str, str]) -> int:
    """A `DESCRIBED_BY` élek: üzemi elem (tag) → eszköz gyökércsúcsa."""
    rows = [{"tag": tag, "device": device_uri(doc)} for tag, doc in sorted(mapping.items())]
    with driver.session() as session:
        record = session.run(LINK, rows=rows, corpus=CORPUS_ID).single()
    return int(record["n"]) if record else 0


def load_plant_layer() -> float:
    """Benedek üzemrétegének betöltése a saját betöltőjével; a visszatérési érték az idő."""
    start = time.perf_counter()
    artifacts = load_corpus_artifacts(CORPUS_ID, INGEST_JSON)
    load_corpus(neo4j_settings(), artifacts.load_plan)
    return time.perf_counter() - start


def load_all() -> dict[str, Any]:
    """A teljes betöltés; a visszatérési érték a mérési jelentés."""
    mapping = tag_mapping()
    present, missing = available(mapping)
    started = time.perf_counter()
    with open_driver() as driver:
        neo4j_load.reset(driver)
        reset_s = time.perf_counter() - started
        devices = load_devices(driver, present)
        plant_s = load_plant_layer()
        links = link_tags(driver, {t: d for t, d in mapping.items() if d in present})
        counts = layer_counts(driver, CORPUS_ID)
    total_s = time.perf_counter() - started
    return {
        "documents_loaded": present,
        "documents_missing_graph": missing,
        "described_by_edges": links,
        "seconds": {"reset": reset_s, "plant_layer": plant_s, "total": total_s},
        "device_seconds": devices,
        "counts": counts,
    }


def main() -> None:
    """Belépési pont: betölt, és kiírja a jelentést."""
    report = load_all()
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
