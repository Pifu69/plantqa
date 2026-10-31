# Eredmények (minden szám forrása)

Minden dokumentumba, ábrára vagy diára kerülő szám egy itteni sorból jön. Oszlopok: EXP-azonosító,
dátum, mit mértünk (modell ID-vel), parancs, kimeneti mappa, eredmény. A két forrásrepó számait
csak a saját `_results.md`-jükre / README-jükre hivatkozva idézzük.

| EXP | Dátum | Mi | Modell | Parancs | Kimenet | Eredmény |
|---|---|---|---|---|---|---|
| EXP-001 | 2026-10-31 | Azure DI elemzés (01. lépés) a 3 új adatlapon | Azure `prebuilt-layout` | `bash scripts/datasheet_pipeline.sh <doc> …` | `data/datasheets/<doc>/01-azure/` | 2 + 16 + 11 = 29 oldal; listaáras költség 0,30 USD (`logs/koltseg.jsonl`) |
| EXP-002 | 2026-10-31 | A példa P&ID generálása: seedkeresés 1-től, Benedek v1 generátora | – (nincs LLM) | `uv run python -m plantqa.plant.generate` | `data/plant/` | elfogadott seed 6 (az 1–5. seed elvetve, `seed_search.json`); 26 tagelt elem, 4 lap, 4 lapközi csatlakozópár, 36 üzemi csúcs, 116 kapcsolat; G1 (visszaépítés) egyezik |
| EXP-003 | 2026-10-31 | Rajzexport | – | `uv run python -m plantgraph.demo.drawing --corpus PQA --corpora-root data/plant/corpora --out data/plant/drawings` | `data/plant/drawings/PQA/` | 4 oldal, 38 szimbólum, 34 vonal, 8 lapközi jel (mind összekötve), 0 átfedés |
