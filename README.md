# plantqa

Joint question answering over a P&ID **and** the vendor datasheets of its tagged items. It merges two
thesis codebases without modifying them (both are imported as uv path dependencies):

- [`../plantdocs`](../plantdocs) (Szabó Zsombor István): vendor datasheet PDF → ISO 15926 / QUDT knowledge
  graph; question answering with method A2 (Neo4j + Cypher).
- [`../Thesis`](../Thesis) (Kiszely Benedek, package `plantgraph`): seeded P&ID generator, sheet splitting
  with off-page connectors, Neo4j store, cascade QA (`cascade_v4_iso`).

The example plant (corpus `PQA`, 26 tagged items, 4 sheets) is generated with plantgraph's v1 generator;
every tagged physical item has a datasheet (`data/plant/tag_to_datasheet.json`). Three methods answer
questions about it:

| Method | What it is |
|---|---|
| **M1** — one graph | plantgraph's `cascade_v4_iso` over the merged Neo4j graph: the Cypher tier sees both schemas, the agent gets a new `datasheet_fact(tag, question)` primitive backed by plantdocs A2 |
| **M2** — router | an agent with two tools: plantgraph's cascade for the drawing, plantdocs A2 for the datasheet of a tag |
| **M3** — baseline | no graph: the serialized drawing (plantgraph ContextRAG) plus datasheet text chunks retrieved by embedding |

Every number in the documents comes from `docs/eredmenyek.md`; decisions are in `docs/dontesek.md`.

## Setup

Python 3.12+, [uv](https://docs.astral.sh/uv/), a local **Neo4j** (tested with 2026.09 Community) with the
neosemantics (n10s) plugin, and the two source repositories next to this one (`../plantdocs`, `../Thesis`).

```powershell
uv sync --extra dev
```

`.env` (never committed; see `.env.example`): `OPENROUTER_API_KEY`, `NEO4J_URI`, `NEO4J_USER`,
`NEO4J_USERNAME`, `NEO4J_PASSWORD`, `NEO4J_DATABASE`.

## Running the demo

```powershell
uv run python -m plantqa.graph.load        # once: loads the merged graph (wipes the Neo4j database!)
uv run python -m plantqa.app               # http://127.0.0.1:8010
```

Left: the P&ID drawing. Right: question, method (M1/M2/M3) and model (GLM-5.3 Flash or GPT-6 Luna); the
answer shows the method, the route (which tier or tool answered), the queries and the datasheet source
pages (click to open the PDF page). `--replay-only` answers only from the LLM cache (no paid calls).

## Reproducing everything

```powershell
uv run python -m plantqa.plant.generate                       # example P&ID (seed search), tag map
uv run python -m plantgraph.demo.drawing --corpus PQA --corpora-root data/plant/corpora --out data/plant/drawings
bash scripts/datasheet_pipeline.sh <document_id> <prefix> "<title>"   # plantdocs pipeline for a new datasheet
uv run python -m plantqa.graph.load [--allow-paid]            # merged graph (+ embeddings of new texts)
uv run python -m plantqa.questions.build                      # question set (dev 20 / frozen test 40)
uv run python -m plantqa.eval.run --exp EXP-0xx --method M1 --model glm --split dev [--allow-paid]
uv run python -m plantqa.eval.score export --exp EXP-0xx      # blind judge packages
uv run python -m plantqa.eval.score merge --exp EXP-0xx       # program + judge verdicts
uv run python -m plantqa.eval.report --exp EXP-0xx            # summary.csv / summary.md / routes.csv
uv run python -m plantqa.figures                              # every figure from the result files
uv run python -m plantqa.costlog status                       # money spent of the 20 USD cap
```

All LLM calls are cached (`data/cache/`): a rerun replays without paying. Paid calls need `--allow-paid`,
go through the shared ledger `logs/koltseg.jsonl`, and stop at 18 USD (new runs) / 20 USD (any call).

## Checks

```powershell
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

## Continuing the work

- **Source repositories:** clone them next to this one, at the commits the results were measured with:
  - `../plantdocs` from [Pifu69/plantdocs](https://github.com/Pifu69/plantdocs), commit `3e46101`. It is
    private, so ask for access.
  - `../Thesis` from [kiszely-benedek/Thesis](https://github.com/kiszely-benedek/Thesis), commit
    `28ba910`.

  Both are read-only for this project.
- **State and rules:** read these in order:
  1. `PROMPT.md`: the task and its hard rules.
  2. `STATUS.md`: what is done and what was left out, and why.
  3. `docs/dontesek.md`: decisions.
  4. `docs/eredmenyek.md`: every measured number, one row per EXP.
  5. `docs/szamellenorzes.md`: the number audit of the thesis.

  A new session can start with: "Read PROMPT.md, STATUS.md and docs/dontesek.md, then continue."
- **Thesis:** the Markdown sources are in `dolgozat/src/`. The first version is kept in `dolgozat/v1/`.
  To rebuild:
  ```powershell
  cd dolgozat/build; npm install; cd ../..
  node dolgozat/build/build.js
  powershell -ExecutionPolicy Bypass -File dolgozat/build/to_pdf.ps1 dolgozat/dolgozat.docx dolgozat/dolgozat.pdf
  ```
  The PDF conversion needs Word.
- **Slides:** to rebuild:
  ```powershell
  cd eloadas/build; npm install; cd ../..
  node eloadas/build/build.js
  ```
  The PDF conversion uses PowerPoint, via `eloadas/build/to_pdf.ps1`.
- **Without an API key:** everything measured so far replays from `data/cache/`.

## Layout

```
src/plantqa/
  plant/      example plant: config, seed search, tag → datasheet map
  graph/      merged Neo4j graph: loader, layer counts
  questions/  question set builder (four families)
  llm/        pins, per-question meter, cached + metered clients for both repos
  methods/    datasheet A2 on the merged graph, cascade wrapper, M1, M2, M3
  eval/       runner, scoring, report
  app/        demo web app
  figures.py  all figures
data/         plant, datasheets (pipeline outputs), questions, caches
runs/         every measurement (answers, verdicts, summaries)
docs/         survey, decisions, results (Hungarian)
dolgozat/     thesis (PDF), eloadas/ presentation (pptx)
```
