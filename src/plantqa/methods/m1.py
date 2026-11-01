"""M1 — egy gráf, egy lekérdezés: Benedek `cascade_v4_iso`-ja az összevont gráfon.

Két kiegészítés, Benedek kódjának módosítása nélkül:
1. A Cypher-lépés sémaszövege az adatlapréteg leírásával bővül (a plantdocs A2
   `qa-cypher` promptjának gráfmodell-része, a `DESCRIBED_BY` kapcsolat és a tagek listája).
2. Az ágens új primitívet kap: `datasheet_fact(tag, question)` a tag eszközgráfjából a
   plantdocs A2 logikájával kér le tényt (`methods.datasheet`). A primitív Benedek
   tool-regiszterébe kerül, így az ágens promptja a regiszterből írt eszközlistában látja.
"""

from __future__ import annotations

import json
import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from plantdocs.qa.context import prompt
from plantgraph.qa.graph_view import GraphView
from plantgraph.qa.harness.registry import CypherDeps, LlmDeps, build_strategy
from plantgraph.qa.plant_api.primitives import PlantApi
from plantgraph.qa.plant_api.tool_registry import TOOLS, ToolSpec
from plantgraph.qa.strategies.base import Strategy
from pydantic import BaseModel, ConfigDict

from plantqa.graph.load import tag_mapping
from plantqa.llm import meter
from plantqa.llm.clients import plantgraph_client
from plantqa.llm.pins import ModelKey
from plantqa.methods.base import MethodAnswer, Question
from plantqa.methods.cascade import AGENT, DrawingCascade, StrategyFactory
from plantqa.methods.datasheet import DatasheetQA

TOOL_NAME = "datasheet_fact"
TOOL_DESCRIPTION = (
    "Ask the vendor datasheet of the item with this tag (pump, valve, transmitter, heat "
    "exchanger, ...) one question about its specification, e.g. a pressure or temperature "
    "limit, a material, a size or an option; returns the datasheet's answer with its PDF pages. "
    "Use it for every property the drawing does not show; first find the tag on the drawing."
)
LINK_TEXT = """DATASHEET LAYER (the same database also holds the datasheet of each tagged item)
- (:PlantItem {tag})-[:DESCRIBED_BY]->(device:Resource) joins a drawn item to the root node of its
  datasheet graph. Several tags can share one datasheet graph (the same product). An item without
  DESCRIBED_BY has no datasheet (e.g. a controller function).
- Every datasheet node has the property document_id (one value per datasheet) and a uri that
  starts with 'urn:plantdocs:<document_id>:'. Parts: (part)-[:lis__partOf]->(device).
- For the facts of a tag: MATCH (p:PlantItem {tag: 'X'})-[:DESCRIBED_BY]->(dev)
  MATCH (d) WHERE d.document_id = dev.document_id AND (d:plm__PCA_100029511 OR
  d:plm__PCA_100029508 OR d:plm__PCA_100029510) ... and filter d by the words of the question.
- Filter broadly (several keywords joined with OR, synonyms, units) and return every matching
  fact with its value, unit, condition, footnote and page: a datasheet value is only correct
  together with its condition, and a question about options or variants needs all of them.
The datasheet graphs follow this model:"""


class DatasheetFactArgs(BaseModel):
    """Az új primitív argumentumai."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    tag: str
    question: str


class DatasheetResult(BaseModel):
    """Az új primitív eredménye, Benedek eredményosztályainak felületével (`render`)."""

    model_config = ConfigDict(frozen=True)

    handle: str
    text: str
    touched_keys: tuple[str, ...] = ()

    def render(self, max_chars: int = 32000, max_items: int = 400) -> str:
        """Az adatlap válasza, a hosszkorláttal levágva."""
        return self.text[:max_chars]


def datasheet_schema() -> str:
    """Az adatlapréteg leírása: kapcsolat, A2 gráfmodell, A2 lekérdezési szabályok, tagek.

    A lekérdezési szabályok (a plantdocs `qa-cypher` RULES része) EXP-011-től kerülnek be.
    """
    text = prompt("qa-cypher")
    model = text[text.index("GRAPH MODEL") : text.index("WHAT IS IN THIS GRAPH")].strip()
    rules = text[text.index("RULES") : text.index("- Answer with the query only")].strip()
    by_doc: dict[str, list[str]] = {}
    for tag, doc in sorted(tag_mapping().items()):
        by_doc.setdefault(doc, []).append(tag)
    docs = "\n".join(f"- {doc}: {', '.join(tags)}" for doc, tags in sorted(by_doc.items()))
    head = f"{LINK_TEXT}\n{model}\nDatasheets and the tags they describe:\n{docs}"
    return f"{head}\nDATASHEET QUERY {rules}"


class DatasheetTool:
    """A `datasheet_fact` primitív: tag → dokumentum → plantdocs A2; a forrásokat gyűjti."""

    def __init__(self, qa: DatasheetQA) -> None:
        """A tag → dokumentum hozzárendelés a programmal előállított fájlból."""
        self.qa, self.mapping = qa, tag_mapping()
        self.calls: list[dict[str, Any]] = []

    def run(self, api: PlantApi, args: DatasheetFactArgs) -> DatasheetResult:
        """Egy tényhívás; ismeretlen vagy adatlap nélküli tagre szöveges választ ad."""
        doc = self.mapping.get(args.tag)
        if doc is None:
            text = f"No datasheet is linked to tag {args.tag!r} (not a documented item)."
            return DatasheetResult(handle=TOOL_NAME, text=text)
        try:
            result = self.qa.ask(doc, args.question, qid=f"m1/{args.tag}")
        except FileNotFoundError:
            text = f"The datasheet graph of {doc} (tag {args.tag}) is not available."
            return DatasheetResult(handle=TOOL_NAME, text=text)
        call = {"tag": args.tag, "document_id": doc, "query": result["query"]}
        self.calls.append({**call, "pages": result["pages"]})
        pages = ", ".join(map(str, result["pages"][:8]))
        text = f"Datasheet {doc} (tag {args.tag}), pages {pages}:\n{result['answer']}"
        return DatasheetResult(handle=TOOL_NAME, text=text)

    def spec(self) -> ToolSpec:
        """A regiszterbe kerülő eszközleírás."""
        return ToolSpec(TOOL_NAME, TOOL_DESCRIPTION, DatasheetFactArgs, self.run)  # type: ignore[arg-type]


@contextmanager
def registered(tool: DatasheetTool) -> Iterator[None]:
    """Az eszköz a regiszterben a blokk idejére (az ágens promptja ekkor készül)."""
    TOOLS[TOOL_NAME] = tool.spec()
    try:
        yield
    finally:
        TOOLS.pop(TOOL_NAME, None)


def extended_strategies(tool: DatasheetTool) -> Any:
    """Benedek stratégiái; az ágens a regiszterbe jegyzett új primitívvel épül fel."""

    def factory(view: GraphView) -> StrategyFactory:
        def make(name: str, params: dict[str, Any], llm: LlmDeps, cypher: CypherDeps) -> Strategy:
            if name != AGENT:
                return build_strategy(name, params, view, cypher, llm)
            with registered(tool):
                return build_strategy(name, params, view, cypher, llm)

        return make

    return factory


def cypher_queries(traces: list[dict[str, Any]]) -> list[str]:
    """A Cypher-lépés lekérdezései a nyomokból."""
    out = []
    for tier in traces:
        retrieval = tier["trace"].get("retrieval")
        if isinstance(retrieval, dict) and retrieval.get("cypher"):
            out.append(str(retrieval["cypher"]))
    return out


class M1:
    """Egy gráf, egy lekérdezés (kiegészített cascade)."""

    name = "M1"

    def __init__(self, model: ModelKey, allow_paid: bool) -> None:
        """A cascade a kiegészített sémával és az új primitívvel."""
        self.model = model
        self.tool = DatasheetTool(DatasheetQA(model, allow_paid))
        self.cascade = DrawingCascade(
            model,
            plantgraph_client(allow_paid),
            f"M1-{model}",
            extra_schema=datasheet_schema(),
            strategies=extended_strategies(self.tool),
        )

    def ask(self, question: Question) -> MethodAnswer:
        """Egy kérdés: a cascade fut, az ágens futás közben a regiszterből hívja a primitívet."""
        self.tool.calls = []
        usage, started = meter.start(), time.perf_counter()
        with registered(self.tool):
            result, traces = self.cascade.ask(
                question.qid, question.text, question.answer_type, question.label
            )
        final = getattr(result, "final_answer", None)
        route = [t["tier"] for t in traces] + [f"{TOOL_NAME}:{c['tag']}" for c in self.tool.calls]
        sources = [{"document_id": c["document_id"], "pages": c["pages"]} for c in self.tool.calls]
        return MethodAnswer(
            method=self.name,
            model=self.model,
            final=final.model_dump(mode="json") if final is not None else None,
            outcome=str(getattr(getattr(result, "outcome", None), "value", "NEEDS_PAID_CALL")),
            route=route,
            cypher=cypher_queries(traces) + [c["query"] for c in self.tool.calls],
            sources=sources,
            latency_s=time.perf_counter() - started,
            usage=usage.as_dict(),
            trace=json.loads(json.dumps(traces, default=str)),
        )
