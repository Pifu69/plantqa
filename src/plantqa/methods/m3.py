"""M3 — baseline: gráf nélküli RAG.

A kontextus: Benedek ContextRAG-jának szerializált üzeme (`serialize_occurrence_graph`, az
egész rajz a promptban, a ChatP&ID-módszer) és a kérdéshez vektoros kereséssel választott
adatlap-darabok (`methods.chunks`). Egy hívás, a ContextRAG-hoz hasonlóan magas gondolkodással.
"""

from __future__ import annotations

import time

from plantgraph.llm.models import ChatMessage, ChatRequest
from plantgraph.qa.corpus import load_corpus_artifacts
from plantgraph.qa.graph_view import NetworkxGraphView
from plantgraph.qa.serialize import serialize_occurrence_graph

from plantqa.graph.load import INGEST_JSON, tag_mapping
from plantqa.llm import meter
from plantqa.llm.clients import plantgraph_client
from plantqa.llm.pins import ModelKey, pin
from plantqa.methods.base import (
    GROUNDING_RULE,
    MethodAnswer,
    Question,
    format_instruction,
    parse_final,
)
from plantqa.methods.chunks import ChunkIndex
from plantqa.plant.spec import CORPUS_ID

TOP_K = 12
PROMPT = """You answer questions about one industrial plant from its documents: the P&ID drawing
(given below as a serialized graph: one node per symbol drawn on a sheet, with its tag and
class, edges for pipes and signals, off-page connectors joining sheets) and excerpts of the
vendor datasheets of its items (retrieved by similarity; each excerpt names its datasheet and
page). Which datasheet belongs to which tag: {mapping}.

Answer using only these documents. If they do not contain the answer, do not guess: set
not_present to true. {rule}

P&ID (serialized graph):
{plant}

Datasheet excerpts:
{excerpts}

Question:
{question}

{fmt}
Reply with exactly one JSON object and nothing else:
{{"answer": <your answer, or null if not_present is true>, "not_present": <true or false>}}"""


def mapping_text() -> str:
    """Melyik adatlap melyik tageké, egy sorban."""
    by_doc: dict[str, list[str]] = {}
    for tag, doc in sorted(tag_mapping().items()):
        by_doc.setdefault(doc, []).append(tag)
    return "; ".join(f"{d}: {', '.join(t)}" for d, t in sorted(by_doc.items()))


class M3:
    """Gráf nélküli baseline: egész rajz + visszakeresett adatlap-darabok."""

    name = "M3"

    def __init__(self, model: ModelKey, allow_paid: bool) -> None:
        """A rajz szerializálása egyszer, a darabindex felépítése."""
        self.model = model
        self.client = plantgraph_client(allow_paid)
        self.pin = pin(model, "high")
        a = load_corpus_artifacts(CORPUS_ID, INGEST_JSON)
        view = NetworkxGraphView(CORPUS_ID, a.localized_sheets, a.resolution)
        self.plant = serialize_occurrence_graph(view).text
        self.index = ChunkIndex(allow_paid)
        self.mapping = mapping_text()

    def _prompt(self, question: Question, found: list[dict[str, object]]) -> str:
        excerpts = "\n\n".join(f"[{c['document_id']}, p. {c['page']}]\n{c['text']}" for c in found)
        return PROMPT.format(
            mapping=self.mapping,
            plant=self.plant,
            excerpts=excerpts,
            question=question.text,
            fmt=format_instruction(question.answer_type),
            rule=GROUNDING_RULE,
        )

    def ask(self, question: Question) -> MethodAnswer:
        """Egy hívás a teljes kontextussal."""
        usage, started = meter.start(), time.perf_counter()
        found = self.index.search(question.text, TOP_K)
        text = self._prompt(question, found)
        message = ChatMessage(role="user", content=text)
        request = ChatRequest(pin=self.pin, messages=[message], purpose="answer")
        reply = self.client.complete(request, run_id=f"M3-{self.model}", question_id=question.qid)
        final = parse_final(reply.text)
        pages: dict[str, list[int]] = {}
        for c in found:
            pages.setdefault(str(c["document_id"]), []).append(int(c["page"]))
        chunks = [{k: c[k] for k in ("document_id", "page", "score")} for c in found]
        return MethodAnswer(
            method=self.name,
            model=self.model,
            final=final,
            outcome="ANSWERED" if final else "PARSE_FAILURE",
            route=["context_rag+chunks"],
            sources=[{"document_id": d, "pages": p} for d, p in pages.items()],
            latency_s=time.perf_counter() - started,
            usage=usage.as_dict(),
            trace={"chunks": chunks, "prompt_chars": len(text), "reply": reply.text},
        )
