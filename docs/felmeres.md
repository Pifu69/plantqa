# Felmérés (0. fázis, 2026-10-31)

A két forrásrepó csak olvasható; a plantqa mindkettőt uv path-függőségként importálja
(`plantdocs[graph,app,extract,azure]`, `plantgraph`). Ellenőrizve: mindkét csomag importálható
a plantqa környezetéből (Python 3.13, uv 0.12.17), a helyi Neo4j fut (Community 2026.09.0,
Cypher 5 és 25, n10s plugin; egyetlen felhasználói adatbázis: `neo4j`).

## 1. A két Neo4j-séma

### plantdocs A2 (eszközgráf, egy adatlap)

- Forrás: `rdf/convert.py` → TTL, betöltés n10s-sel: `plantdocs/graph/neo4j_load.py`
  (`reset(driver)` az egész adatbázist törli és beállítja az n10s-t, `load(driver, turtle)`
  importál). Kapcsolat: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`; mindig az alapadatbázis.
- Minden csúcs `:Resource {uri}` (egyedi kulcs: `n10s_unique_uri`); az `rdf:type` további
  címkéket ad (`handleVocabUris: SHORTEN`, pl. `plm__PCA_100029511`).
- Eszköz-gyökércsúcs: `uri = "urn:plantdocs:<document_id>:device"`, címkék
  `:Resource:lis__PhysicalObject:plm__PCA_<osztály>`, `rdfs__label` = eszköznév. Az alkatrészek
  is `lis__PhysicalObject`, `-[:lis__partOf]->` az eszközre. `document_id` tulajdonság
  **nincs**, csak az URI-kban (`urn:plantdocs:<doc>:…`).
- Adatpontok (ISO 15926 / POSC Caesar Datasheet Ontology): Quantity Datum `PCA_100029511`,
  Attribute Datum `PCA_100029508`, Classification Datum `PCA_100029510`, Datum (lábjegyzet)
  `PCA_100029505`, Case Datum `PCA_100029512`, Section Datum `PCA_100029513`, Case
  `PCA_100029524`. Tulajdonságok: `plm__PCA_100029521` (nyomtatott címke),
  `plm__PCA_100029522` (nyomtatott érték), `lis__datumValue`, `qudt__lowerBound`/`upperBound`,
  `schema__pageStart` (PDF-oldal).
- Kapcsolatok: `plm__PCA_100029506` (adatlap tartalmaz), `plm__PCA_100029516` (alany:
  eszköz/alkatrész), `plm__PCA_100029519` (szabványos attribútum), `plm__PCA_100029520`
  (eset), `plm__PCA_100029525` (forrásszakasz), `lis__datumUOM` (egység, QUDT-re
  `skos__exactMatch`). Az LLM-nek szóló leírás: `prompts/qa-cypher.md`.
- Vektorindex: `plantdocs_vectors` a `Resource.embedding`-en (512 dim., koszinusz,
  `qwen/qwen3-embedding-8b`), `graph/vectors.py`.

### plantgraph (Benedek, üzemi réteg)

- Betöltés: `store/neo4j_loader.load_corpus(settings, plan)`; a terv
  `qa/corpus.load_corpus_artifacts(corpus_id, ingest.json).load_plan`. **Csak a saját
  korpuszát törli** (`MATCH (n:CorpusNode {corpus_id})`). Kapcsolat: `NEO4J_URI`,
  `NEO4J_USERNAME`, `NEO4J_PASSWORD`, `NEO4J_DATABASE`.
- Profil: a V2T-A rendszer a `plant_lines` profilt olvassa. Minden üzemi elem egy
  `(:CorpusNode:PlantItem {uid, corpus_id, tag, node_class, kind, …})` csúcs, osztálycímkékkel
  (pl. `:PlantItem:CentrifugalPump:Pump:Equipment`); `Sheet`, `DrawingSet`, `PlantSection`,
  `ProcessPlant` szerkezeti csúcsok. Kulcs: `corpus_node_uid` egyediség, index a `corpus_id`-n
  és a `tag`-en.
- Kapcsolatok: `send_to` (anyagáram, csőrészenként), `line_to` (a jelöletlen idomokat átugorja,
  `via_tags`, `n_fittings`), `send_signal_to`, `measured_by`, `control`, `is_located_in`,
  `is_drawn_on`, `has_sheet`; a lapot átlépő élen `crossed_sheets`. A teljes, az LLM-nek adott
  sémaszöveg: `qa/schema_text.build_schema_text(plan)`.

### Összekötés (2. fázis)

`(:CorpusNode:PlantItem {tag})-[:DESCRIBED_BY]->(:Resource {uri: "urn:plantdocs:<doc>:device"})`,
és az eszközgráf minden csúcsa `document_id` tulajdonságot kap (névtér). Több tag mutathat
ugyanarra az eszközgráfra (pl. minden szivattyú a Gorman-Rupp adatlapra).

## 2. A két QA belépési pont

- **plantdocs A2**: `qa/run.py: ask_graph(client, "A2", q, context, run, on_text, sections,
  similar) -> dict` (`answer`, `query`, `rows`, `pages`, `attempts`); `context =
  qa.context.inventory(rdflib.Graph)`, `run = cypher_executor()`, `sections =
  qa.sections.catalog(g)`. Tokent, költséget nem ad vissza, azok a kliens JSONL-naplójában
  vannak (`llm/openrouter.Client`, modell rögzítve: `z-ai/glm-5.3-flash`). Az app motorja
  (`app/engine.py`) dokumentumonként `reset`-el, ezért az összevont gráfon közvetlenül nem
  használható.
- **plantgraph cascade**: a legújabb mért policy a `cascade_v4_iso` (V2T-A rendszer, ADR-0061;
  a legutóbbi commitok — `c51c83e`, `fdad31f`, `87eb79e` — a V2T-A ellenőrző mérését és az R4
  létrát rögzítik ezzel a policyval; a `cascade_v4_iso`-t a `tune_select.py` előre rögzített
  szabálya választotta a `cascade_v4` helyett). Tierjei: `cypher-v2t` (`cypher_rag_lines`,
  30 s lekérdezési időkorlát, 1000 sor) és `agent-v2t` (`graph_agent_lines`, legfeljebb 40
  lépés); a `UPSTREAM/DOWNSTREAM_TO_FIRST_VALVE` kérdések az ágensnél indulnak. Futtatás:
  `qa/cascade/live.LiveCascade(corpus_id, policy, tiers).ask(asked)`; a címke szerinti
  útválasztást a live változat elutasítja, ezt a plantqa a kérdéscsaládból végzi el.
  Pinek: Cypher `openai/gpt-6-luna` reasoning low (`data/runs/exp0007/inputs/
  pin_cypher_luna_low.json`), ágens ugyanez reasoning high (`pin_agent_luna_final_high.json`);
  GLM: `data/runs/cv1/pin_low.json` (`z-ai/glm-5.3-flash`, temperature 0, reasoning low).
- **Baseline**: Benedek `qa/strategies/context_rag.py` (az egész üzem a promptban,
  ChatP&ID-módszer); a plantdocs-ban nincs nyers szöveges darabolós RAG, csak a gráfcsúcsok
  vektoros keresése és a teljes dokumentumos `ask_baseline`.

## 3. Eszköztípus → DEXPI-osztály

| plantdocs eszköz (document_id) | PCA-osztály | DEXPI-osztály (Benedek sémája) |
|---|---|---|
| gorman-rupp-0700286 | Centrifugal Pump | `CentrifugalPump` (P-) |
| fisher-et-d100022x012 | Valve | `GlobeValve` szabályozókörben (FV-/PV-) |
| gfps-165-solenoid-valve | Solenoid Valve | `GlobeValve` kör nélkül (GV-) |
| rosemount-3051-00813-0100-4001 | Transmitter | `ProcessSignalGeneratingFunction` (PT-, FT-) |
| flowserve-worcester-f51-f52 (új) | Ball Valve | `BallValve` (BV-) |
| swagelok-ms-01-176 (új) | Check Valve | `CheckValve` (CHV-) |
| alfalaval-m3 (új) | Plate Heat Exchanger | `HeatExchanger` (E-) |

A szabályozófunkciókhoz (`ProcessInstrumentationFunction`, FIC-/PIC-) nincs gyártói adatlap
(DCS-funkció); ezt a `data/plant/tags.json` indoklással rögzíti.

## 4. Benedek generátorai

- **v1** (`benchmark/generator.py`, `GeneratorConfig`): berendezés `CentrifugalPump`,
  `Compressor`, `Tank`, `PressureVessel`, `ProcessColumn`, `HeatExchanger` (súlyozható:
  `equipment_weights`); szelep `GlobeValve`, `BallValve`, `CheckValve` (nem súlyozható);
  szabályozókör: távadó (PSGF, `xT`), szabályozó (PIF, `xIC`), működtető (AF), a szabályozott
  szelep `xV` tagot kap; változó: F, L, P, T (nem állítható). Tagformátum `P-1-1`.
- **v2** (`benchmark/v2/`): valósághű folyamatminták (oszlop, reaktor, tolózár, biztonsági
  szelep, mérőórák, leürítők stb.); osztályok szerint nem szűkíthető.
- Lapokra bontás: `benchmark/splitter.py` (`SplitConfig`, off-page csatlakozópárok; a bontás a
  megoldókulcs), feloldás: `resolution/`. Egy hívás: `ingest.pipeline.build_synthetic_corpus`.

## 5. Spend guard és cache

- **plantgraph**: `llm/client.ChatClient` (OpenRouter, `openai` SDK), `llm/cache.SqliteCache`
  (kulcs: a kérés kanonikus hash-e; replay módban fizetés nélkül), `qa/harness/spend_cap.
  SpendGuard` (futásonkénti plafon, foglalással), hívásnapló `calls.jsonl`.
- **plantdocs**: nincs spend guard és nincs válaszcache; a `Client` minden hívást JSONL-be ír
  (`cost_usd` az OpenRouter `usage`-ből). Beágyazás-cache: `<graph>.vectors.json`.
- **plantqa**: közös napló `logs/koltseg.jsonl` (`plantqa.costlog`), teljes keret 20 USD,
  18 USD felett új mérés nem indul.
