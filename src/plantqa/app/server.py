"""A demó FastAPI-szervere: rajz, adatlapok, példakérdések, kérdezés bármelyik módszerrel."""

from __future__ import annotations

import hashlib
import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from plantqa.graph.load import tag_mapping
from plantqa.graph.sources import ROOT, pdf_path
from plantqa.llm.pins import ModelKey, pin
from plantqa.methods.base import Method, Question

STATIC = Path(__file__).parent / "static"
DRAWING = ROOT / "data" / "plant" / "drawings" / "PQA" / "drawings.pdf"
LOG = ROOT / "data" / "app" / "ask-log.jsonl"
DEFAULT = ROOT / "data" / "app" / "default_method.json"
ALLOW_PAID = True

app = FastAPI(title="plantqa")
_methods: dict[tuple[str, str], Method] = {}
_lock = threading.Lock()


class AskBody(BaseModel):
    """A kérdés: szöveg, módszer, modell, válaszalak."""

    question: str
    method: str = "M2"
    model: ModelKey = "glm"
    answer_type: str = "FREE_TEXT"


def method_for(name: str, model: ModelKey) -> Method:
    """A módszer példánya (első kérdésnél felépítve, utána újrahasznosítva)."""
    from plantqa.eval.run import build_method

    key = (name, model)
    if key not in _methods:
        _methods[key] = build_method(name, model, ALLOW_PAID)
    return _methods[key]


def default_method() -> dict[str, str]:
    """Az alapértelmezett módszer és modell (a teszten legjobb; az 5. fázis írja ki)."""
    if DEFAULT.exists():
        return dict(json.loads(DEFAULT.read_text(encoding="utf-8")))
    return {"method": "M2", "model": "glm", "why": "not measured yet"}


@app.get("/")
def index() -> FileResponse:
    """Az egyetlen oldal."""
    return FileResponse(STATIC / "index.html")


@app.get("/api/config")
def config() -> dict[str, Any]:
    """A választható modellek, az alapértelmezés és a tag → adatlap tábla."""
    models = {"glm": pin("glm").model_id, "luna": pin("luna").model_id}
    return {"default": default_method(), "models": models, "tags": tag_mapping()}


@app.get("/api/drawing")
def drawing() -> FileResponse:
    """A P&ID minden lapja egy PDF-ben (Benedek rajzexportja)."""
    return FileResponse(DRAWING, media_type="application/pdf")


@app.get("/api/datasheets/{document_id}/pdf")
def datasheet_pdf(document_id: str) -> FileResponse:
    """Egy adatlap PDF-je (a forrásoldal `#page=N` horgonnyal nyílik)."""
    if document_id not in set(tag_mapping().values()):
        raise HTTPException(404, f"unknown document {document_id!r}")
    return FileResponse(pdf_path(document_id), media_type="application/pdf")


@app.get("/api/examples")
def examples() -> list[dict[str, str]]:
    """Példakérdések a dev halmazból, családonként."""
    rows = (ROOT / "data" / "questions" / "dev.jsonl").read_text(encoding="utf-8").splitlines()
    out = [json.loads(r) for r in rows if r.strip()]
    keep = ("qid", "family", "text", "answer_type")
    return [{k: q[k] for k in keep} for q in out]


@app.post("/api/ask")
def ask(body: AskBody) -> dict[str, Any]:
    """Egy kérdés a választott módszerrel; a válasz, az útvonal, a lekérdezések és a források."""
    if body.method not in ("M1", "M2", "M3"):
        raise HTTPException(400, f"unknown method {body.method!r}")
    qid = "app-" + hashlib.sha256(body.question.encode("utf-8")).hexdigest()[:10]
    question = Question(qid, body.question, body.answer_type)
    with _lock:
        answer = method_for(body.method, body.model).ask(question)
    result = {**answer.as_dict(), "text": answer.text(), "model_id": pin(body.model).model_id}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    row = {"time": datetime.now(UTC).isoformat(timespec="seconds"), "question": body.question}
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({**row, **result}, ensure_ascii=False, default=str) + "\n")
    return result
