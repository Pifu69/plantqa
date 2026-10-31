"""Az M3 adatlap-darabjai: a PDF-ek szövege oldalanként, darabolva, vektorokkal (gráf nélkül).

A beágyazás a plantdocs modellje és dimenziója (`qwen/qwen3-embedding-8b`, 512), a plantdocs
`Embedder`-én és a plantqa cache-elt szállítóján át; a vektorok szövegenként cache-elve.
"""

from __future__ import annotations

import base64
import json
import math
from array import array
from pathlib import Path
from typing import Any

import pymupdf
from plantdocs.llm.embeddings import DIMENSIONS, MODEL, Embedder

from plantqa.graph.load import tag_mapping
from plantqa.graph.sources import ROOT, pdf_path
from plantqa.llm.clients import CACHE_DIR, plantdocs_embed_transport

CHUNK_DIR = ROOT / "data" / "chunks"
MAX_CHARS = 1500


def _pieces(text: str) -> list[str]:
    """Egy oldal szövege legfeljebb `MAX_CHARS` hosszú, bekezdéshatáron vágott darabokra."""
    pieces, current = [], ""
    for paragraph in (p.strip() for p in text.split("\n\n")):
        if current and len(current) + len(paragraph) > MAX_CHARS:
            pieces.append(current)
            current = ""
        current = f"{current}\n\n{paragraph}".strip()[: MAX_CHARS * 2]
    return [*pieces, current] if current else pieces


def document_chunks(document_id: str) -> list[dict[str, Any]]:
    """Egy adatlap darabjai oldalszámmal."""
    doc: Any = pymupdf.open(pdf_path(document_id))  # type: ignore[no-untyped-call]
    out = []
    for number in range(1, int(doc.page_count) + 1):
        for piece in _pieces(str(doc[number - 1].get_text())):
            out.append({"document_id": document_id, "page": number, "text": piece})
    return out


def all_chunks() -> list[dict[str, Any]]:
    """Az üzem összes adatlapjának darabjai, dokumentum szerint rendezve."""
    documents = sorted(set(tag_mapping().values()))
    return [chunk for doc in documents for chunk in document_chunks(doc)]


def _pack(vector: list[float]) -> str:
    return base64.b64encode(array("f", vector).tobytes()).decode("ascii")


def _unpack(text: str) -> list[float]:
    return array("f", base64.b64decode(text)).tolist()


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0


class ChunkIndex:
    """A darabok és vektoraik; lekérdezéskor koszinusz-hasonlóság szerinti első `k`."""

    def __init__(self, allow_paid: bool, folder: Path = CHUNK_DIR) -> None:
        """A darabok (újraépítve a PDF-ekből) és a vektorok (cache-ből vagy beágyazva)."""
        self.embedder = Embedder(CACHE_DIR / "plantdocs-embed-calls.jsonl")
        self.embedder.transport = plantdocs_embed_transport(allow_paid)
        self.chunks = all_chunks()
        self.vectors = self._vectors(folder / "vectors.json")

    def _vectors(self, path: Path) -> list[list[float]]:
        cache: dict[str, str] = {}
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            cache = data["items"] if data.get("model") == MODEL else {}
        texts = [c["text"] for c in self.chunks]
        missing = sorted({t for t in texts if t not in cache})
        fresh = self.embedder.embed(missing, tag="plantqa/M3/chunks") if missing else []
        cache |= {t: _pack(v) for t, v in zip(missing, fresh, strict=True)}
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"model": MODEL, "dimensions": DIMENSIONS, "items": cache}
        path.write_text(json.dumps(payload), encoding="utf-8")
        return [_unpack(cache[t]) for t in texts]

    def search(self, question: str, k: int) -> list[dict[str, Any]]:
        """A kérdéshez legközelebbi `k` darab, hasonlósággal."""
        query = self.embedder.embed([question], tag="plantqa/M3/question")[0]
        scored = [(_cosine(query, v), i) for i, v in enumerate(self.vectors)]
        best = sorted(scored, reverse=True)[:k]
        return [{**self.chunks[i], "score": round(s, 4)} for s, i in best]
