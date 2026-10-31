"""M2 — router: egy ágens két eszközt hív, majd összerakja a választ.

Eszközök: `drawing(question)` → Benedek `cascade_v4_iso`-ja a rajzon (változtatás nélkül),
`datasheet(tag, question)` → a tagből feloldott eszköz plantdocs A2-je. A router minden
lépésben egy JSON-objektumot ír; legfeljebb `MAX_STEPS` eszközhívás után válaszolnia kell.
"""

from __future__ import annotations

import json
import time
from typing import Any

from plantgraph.llm.client import ChatClient
from plantgraph.llm.models import ChatMessage, ChatRequest, ProviderError

from plantqa.graph.load import tag_mapping
from plantqa.llm import meter
from plantqa.llm.clients import plantgraph_client
from plantqa.llm.pins import ModelKey, pin
from plantqa.methods.base import (
    GROUNDING_RULE,
    MethodAnswer,
    Question,
    complete_with_retry,
    format_instruction,
    parse_final,
)
from plantqa.methods.cascade import DrawingCascade
from plantqa.methods.datasheet import DatasheetQA

MAX_STEPS = 6
SYSTEM = """You answer questions about one industrial plant. You cannot see the documents
yourself; you have two tools:
- drawing(question): answers a question about the plant's P&ID drawing (which items exist and
  their tags and types, what is connected to what, flow paths, upstream/downstream items,
  which instrument measures what, control loops, units, sheets).
- datasheet(tag, question): answers a question about the vendor datasheet of the item with
  this tag (its specification: pressures, temperatures, materials, sizes, options, ...).
  Items with a datasheet: {tags}.
If a question names an item by its position or role (e.g. "the valve downstream of P-1-1"),
first ask the drawing tool for its tag, then ask the datasheet tool about that tag.
Each turn, reply with exactly one JSON object and nothing else:
{{"tool": "drawing", "question": "..."}}
{{"tool": "datasheet", "tag": "...", "question": "..."}}
{{"final": {{"answer": <answer or null>, "not_present": <true if the documents do not contain
the answer, else false>}}}}
Answer only from the tool results. {rule}
Answer format: {fmt}"""


class Router:
    """A router hurok egy kérdésre: lépésenként egy eszközhívás vagy a végső válasz."""

    def __init__(self, client: ChatClient, model: ModelKey, run_id: str) -> None:
        """A kliens és a router pinje (alacsony gondolkodás)."""
        self.client, self.pin, self.run_id = client, pin(model, "low"), run_id

    def step(self, messages: list[ChatMessage], qid: str) -> str:
        """Egy routerlépés szövege."""
        request = ChatRequest(pin=self.pin, messages=messages, purpose="route")
        return complete_with_retry(self.client, request, self.run_id, qid).text


def _action(reply: str) -> dict[str, Any]:
    """A router válaszának első JSON-objektuma (hibás válasz: üres szótár)."""
    start, end = reply.find("{"), reply.rfind("}")
    try:
        data = json.loads(reply[start : end + 1]) if start >= 0 else {}
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


class M2:
    """Router a két meglévő rendszer fölött."""

    name = "M2"

    def __init__(self, model: ModelKey, allow_paid: bool) -> None:
        """A két eszköz és a router kliense."""
        self.model = model
        client = plantgraph_client(allow_paid)
        self.router = Router(client, model, f"M2-{model}")
        self.drawing = DrawingCascade(model, client, f"M2-drawing-{model}")
        self.datasheet = DatasheetQA(model, allow_paid)
        self.mapping = tag_mapping()

    def _drawing(self, qid: str, text: str, log: dict[str, Any]) -> str:
        result, traces = self.drawing.ask(f"{qid}/d{len(log['route'])}", text, "FREE_TEXT")
        final = getattr(result, "final_answer", None)
        for tier in traces:
            retrieval = tier["trace"].get("retrieval")
            if isinstance(retrieval, dict) and retrieval.get("cypher"):
                log["cypher"].append(str(retrieval["cypher"]))
        log["route"].append("drawing:" + "+".join(t["tier"] for t in traces))
        if final is None:
            return "The drawing tool gave no answer."
        return json.dumps(final.model_dump(mode="json"))

    def _datasheet(self, tag: str, text: str, log: dict[str, Any]) -> str:
        doc = self.mapping.get(tag)
        log["route"].append(f"datasheet:{tag}")
        if doc is None:
            return f"No datasheet is linked to tag {tag!r}."
        try:
            result = self.datasheet.ask(doc, text, qid=f"m2/{tag}")
        except FileNotFoundError:
            return f"The datasheet graph of {doc} is not available."
        log["cypher"].append(result["query"])
        log["sources"].append({"document_id": doc, "pages": result["pages"]})
        return f"Datasheet {doc}, pages {result['pages'][:8]}:\n{result['answer']}"

    def _tool(self, qid: str, action: dict[str, Any], log: dict[str, Any]) -> str:
        if action.get("tool") == "drawing":
            return self._drawing(qid, str(action.get("question", "")), log)
        if action.get("tool") == "datasheet":
            tag, text = str(action.get("tag", "")), str(action.get("question", ""))
            return self._datasheet(tag, text, log)
        return "Unknown action. Reply with one JSON object as described."

    def _messages(self, question: Question) -> list[ChatMessage]:
        tags = ", ".join(sorted(self.mapping))
        system = SYSTEM.format(
            tags=tags, fmt=format_instruction(question.answer_type), rule=GROUNDING_RULE
        )
        return [
            ChatMessage(role="system", content=system),
            ChatMessage(role="user", content=question.text),
        ]

    def ask(self, question: Question) -> MethodAnswer:
        """A router hurok; a végső válasz vagy a lépéskeret kimerülése zárja."""
        usage, started = meter.start(), time.perf_counter()
        messages = self._messages(question)
        log: dict[str, Any] = {"route": [], "cypher": [], "sources": []}
        final: dict[str, Any] | None = None
        outcome = "STEP_LIMIT"
        for _ in range(MAX_STEPS + 1):
            try:
                reply = self.router.step(messages, question.qid)
            except ProviderError:
                outcome = "PROVIDER_ERROR"
                break
            action = _action(reply)
            if "final" in action:
                final = parse_final(json.dumps({"answer": None, **_as_dict(action["final"])}))
                outcome = "ANSWERED" if final else "PARSE_FAILURE"
                break
            observation = self._tool(question.qid, action, log)
            messages = [
                *messages,
                ChatMessage(role="assistant", content=reply),
                ChatMessage(role="user", content=f"Tool result:\n{observation}"),
            ]
        return MethodAnswer(
            method=self.name,
            model=self.model,
            final=final,
            outcome=outcome,
            route=log["route"],
            cypher=log["cypher"],
            sources=log["sources"],
            latency_s=time.perf_counter() - started,
            usage=usage.as_dict(),
            trace=[m.model_dump() for m in messages[1:]],
        )


def _as_dict(value: Any) -> dict[str, Any]:
    """A `final` mező szótárként (ha a modell puszta értéket írt, az a válasz)."""
    return value if isinstance(value, dict) else {"answer": value, "not_present": False}
