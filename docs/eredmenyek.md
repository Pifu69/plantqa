# Eredmények (minden szám forrása)

Minden dokumentumba, ábrára vagy diára kerülő szám egy itteni sorból jön. Oszlopok: EXP-azonosító,
dátum, mit mértünk (modell ID-vel), parancs, kimeneti mappa, eredmény. A két forrásrepó számait
csak a saját `_results.md`-jükre / README-jükre hivatkozva idézzük.

| EXP | Dátum | Mi | Modell | Parancs | Kimenet | Eredmény |
|---|---|---|---|---|---|---|
| EXP-001 | 2026-10-31 | Azure DI elemzés (01. lépés) a 3 új adatlapon | Azure `prebuilt-layout` | `bash scripts/datasheet_pipeline.sh <doc> …` | `data/datasheets/<doc>/01-azure/` | 2 + 16 + 11 = 29 oldal; listaáras költség 0,30 USD (`logs/koltseg.jsonl`) |
| EXP-002 | 2026-10-31 | A példa P&ID generálása: seedkeresés 1-től, Benedek v1 generátora | – (nincs LLM) | `uv run python -m plantqa.plant.generate` | `data/plant/` | elfogadott seed 6 (az 1–5. seed elvetve, `seed_search.json`); 26 tagelt elem, 4 lap, 4 lapközi csatlakozópár, 36 üzemi csúcs, 116 kapcsolat; G1 (visszaépítés) egyezik |
| EXP-003 | 2026-10-31 | Rajzexport | – | `uv run python -m plantgraph.demo.drawing --corpus PQA --corpora-root data/plant/corpora --out data/plant/drawings` | `data/plant/drawings/PQA/` | 4 oldal, 38 szimbólum, 34 vonal, 8 lapközi jel (mind összekötve), 0 átfedés |
| EXP-004 | 2026-10-31 | Kérdéssor: 4 család × 15 (a: Benedek generátora a gold gráfból, seed 1; b: plantdocs EXP-0026/EXP-0039 gold párok tagre leképezve; c: programmal összerakott topológiai lépés + adatlapi gold; d: megválaszolhatatlan), dev 20 / teszt 40, seed 20261031. **A teszthalmaz befagyasztva.** | – | `uv run python -m plantgraph.qa.questions --corpus-id PQA --ingest-json data/plant/corpora/PQA/ingest.json --seed 1 --out data/questions/pool_a --n-per-bin 10 --n-unanswerable 10`, majd `uv run python -m plantqa.questions.build` | `data/questions/` | `dev.jsonl` sha256 `980f6c5e155011092dc3fd00535342f1cf03ffd252577c63879566a239b9d4ae`; `test.jsonl` sha256 `6f3b427cb774f24d45443e6d1b839a82db93d8f6fea7037e26fa2121d0c8979e`. A (b)–(d) referenciaválaszai modellkészítésűek (EXP-0026/0039: claude-opus-5-5, a felhasználó nem ellenőrizte), az (a) és a (c) topológiai része programból jön. |
