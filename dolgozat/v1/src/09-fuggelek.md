# Függelék

## A. Példakérdések családonként (dev halmaz)

Táblázat: Két példakérdés családonként a dev halmazból, a referenciaválasz rövidítve (EXP-004)
| Család | Kérdés | Referenciaválasz (rövidítve) |
|---|---|---|
| (a) | Can process flow reach P-2-2 from P-1-1? | no |
| (a) | Which valve is actuated by control loop PIC-2-1? | PV-2-1 |
| (b) | Regarding P-1-2 on the P&ID: What's the hottest liquid I can put through it? | 160 °F (71 °C) maximum liquid temperature (seal limit); the 250 psi max operating pressure applies only up to 100 °F (37 °C); consult the factory beyond. |
| (b) | Regarding FV-2-2 on the P&ID: What flow characteristics can I get: equal percentage, linear, quick opening? | Standard cages: quick-opening, linear or equal percentage. Whisper Trim, WhisperFlo and Cavitrol cages: linear only. |
| (c) | Consider the item directly upstream of CHV-2-1 in the process flow. What kind of shaft seal does it have, and what's the part number for a replacement seal? | Mechanical, self-lubricated seal: silicon carbide rotating and stationary faces, fluorocarbon (Viton or equivalent) elastomers, 316 stainless shaft sleeve and s |
| (c) | Consider the item directly upstream of CHV-2-2 in the process flow. What is a Fisher ET? Is it the valve body, and what kind of valve is it? | A sliding-stem, single-port globe-style control valve (body) with cage guiding, balanced valve plug and push-down-to-close plug action, for throttling or on-off |
| (d) | Regarding GV-1-2 on the P&ID: It hums but won't open. What could be wrong? | No troubleshooting in the datasheet. Related facts only: it needs at least 0.5 bar differential pressure to open; voltage must match the type plate (±10 %). The |
| (d) | Regarding PV-2-1 on the P&ID: The valve leaks through when shut. Is it the seat ring or the plug seal, and how do I check? | Not in the document (no troubleshooting). |

## B. Az M2 router rendszerüzenete

```
You answer questions about one industrial plant. You cannot see the documents
yourself; you have two tools:
- drawing(question): answers a question about the plant's P&ID drawing (which items exist and
  their tags and types, what is connected to what, flow paths, upstream/downstream items,
  which instrument measures what, control loops, units, sheets).
- datasheet(tag, question): answers a question about the vendor datasheet of the item with
  this tag (its specification: pressures, temperatures, materials, sizes, options, ...).
  Items with a datasheet: <24 tags>.
If a question names an item by its position or role (e.g. "the valve downstream of P-1-1"),
first ask the drawing tool for its tag, then ask the datasheet tool about that tag.
Each turn, reply with exactly one JSON object and nothing else:
{"tool": "drawing", "question": "..."}
{"tool": "datasheet", "tag": "...", "question": "..."}
{"final": {"answer": <answer or null>, "not_present": <true if the documents do not contain
the answer, else false>}}
Answer only from the tool results. If the documents give only part of what is asked, answer with that part and say which part is not stated; set not_present to true only when they contain nothing relevant. Never add advice, procedures, causes or values that the documents do not state.
Answer format: <Benedek answer-format sentence>
```

## C. Az M1 Cypher-szintjének sémakiegészítése (eleje) és az új primitív leírása

```
DATASHEET LAYER (the same database also holds the datasheet of each tagged item)
- (:PlantItem {tag})-[:DESCRIBED_BY]->(device:Resource) joins a drawn item to the root node of its
  datasheet graph. Several tags can share one datasheet graph (the same product). An item without
  DESCRIBED_BY has no datasheet (e.g. a controller function).
- Every datasheet node has the property document_id (one value per datasheet) and a uri that
  starts with 'urn:plantdocs:<document_id>:'. Parts: (part)-[:lis__partOf]->(device).
- For the facts of a tag: MATCH (p:PlantItem {tag: 'X'})-[:DESCRIBED_BY]->(dev)
  MATCH (d) WHERE d.document_id = dev.document_id AND (d:plm__PCA_100029511 OR
  d:plm__PCA_100029508 OR d:plm__PCA_100029510) ... and filter d by the words of the question.
The datasheet graphs follow this model:
Ask the vendor datasheet of the item with this tag (pump, valve, transmitter, heat exchanger, ...) one question about its specification, e.g. a pressure or temperature limit, a material, a size or an option; returns the datasheet's answer with its PDF pages. Use it for every property the drawing does not show; first find the tag on the drawing.
```

A sémakiegészítés ezután a plantdocs A2 `qa-cypher` promptjának GRAPH MODEL és RULES részét és a tagek dokumentumonkénti listáját tartalmazza (`src/plantqa/methods/m1.py`, `datasheet_schema`).
