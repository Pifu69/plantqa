"""Cache-elt, mért és naplózott kliensek mindkét repó LLM-hívásaihoz.

- Benedek `ChatClient`-je: `MeteredChatClient` (alosztály), saját SQLite cache-sel;
  minden válasz a kérdés mérőjébe, az élő hívás költsége a közös naplóba is kerül.
- plantdocs `Client` és `Embedder`: `CachedTransport` (a kérés sha256-ja a kulcs).
Élő hívás csak akkor megy ki, ha a közös keretből van még (`costlog.TOTAL_CAP_USD`).
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from plantdocs.llm import embeddings as pd_embeddings
from plantdocs.llm import openrouter as pd_openrouter
from plantgraph.llm.cache import SqliteCache
from plantgraph.llm.client import ChatClient
from plantgraph.llm.models import ChatRequest, ChatResponse
from plantgraph.llm.openrouter_settings import from_env

from plantqa import costlog
from plantqa.graph.sources import ROOT
from plantqa.llm import meter

CACHE_DIR = ROOT / "data" / "cache"
Transport = Callable[[dict[str, Any]], dict[str, Any]]


def load_env() -> None:
    """A plantqa `.env`-je (a kulcs innen jön; a valódi környezeti változó erősebb)."""
    load_dotenv(ROOT / ".env", override=False)


def _guard_live_call() -> None:
    """Élő hívás előtt: ha a teljes keret elfogyott, megtagadja."""
    if costlog.remaining_usd() <= 0.0:
        raise costlog.BudgetExceeded("the 20 USD budget is used up: no more live calls")


class MeteredChatClient(ChatClient):
    """Benedek kliense, amely minden választ mér és az élő költést naplózza."""

    source = "plantgraph"

    def complete(
        self,
        request: ChatRequest,
        *,
        run_id: str,
        question_id: str | None = None,
        strategy: str | None = None,
        timeout_s: float | None = None,
    ) -> ChatResponse:
        """Mint az ősé; utána mérés és (élő hívásnál) naplósor."""
        response = super().complete(
            request, run_id=run_id, question_id=question_id, strategy=strategy, timeout_s=timeout_s
        )
        cost = float(response.cost_usd or 0.0)
        model = request.pin.model_id
        meter.current().add(
            model, response.prompt_tokens, response.completion_tokens, cost, response.from_cache
        )
        if not response.from_cache:
            costlog.record(
                {
                    "source": self.source,
                    "tag": f"{run_id}/{question_id}/{request.purpose}",
                    "model": model,
                    "prompt_tokens": response.prompt_tokens,
                    "completion_tokens": response.completion_tokens,
                    "cost_usd": cost,
                }
            )
        return response


def plantgraph_client(allow_paid: bool, cache_name: str = "plantgraph.sqlite") -> ChatClient:
    """Benedek kliense a közös cache-sel; `allow_paid=False` esetén csak cache-ből válaszol."""
    load_env()
    settings = from_env()
    if settings is None:
        raise RuntimeError("expected OPENROUTER_API_KEY in the plantqa .env, found none")
    if allow_paid:
        _guard_live_call()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = SqliteCache(CACHE_DIR / cache_name, "live")
    return MeteredChatClient.for_openrouter(
        settings,
        cache=cache,
        calls_log_path=CACHE_DIR / "calls.jsonl",
        allow_network=allow_paid,
    )


class CachedTransport:
    """A plantdocs-kliensek szállítója: SQLite-cache, mérés és naplózás."""

    def __init__(self, live: Transport, source: str, allow_paid: bool, path: Path) -> None:
        """`live` a valódi hívás (plantdocs `http_transport` vagy `http_embed`)."""
        self.live, self.source, self.allow_paid = live, source, allow_paid
        path.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute("CREATE TABLE IF NOT EXISTS calls (key TEXT PRIMARY KEY, answer TEXT)")
        self._lock = threading.Lock()

    def __call__(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Cache-ből, vagy (ha szabad) élő hívással; mindkét esetben mér."""
        key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        with self._lock:
            row = self._db.execute("SELECT answer FROM calls WHERE key = ?", (key,)).fetchone()
        if row is not None:
            answer: dict[str, Any] = json.loads(row[0])
            self._measure(payload, answer, cached=True)
            return answer
        if not self.allow_paid:
            raise costlog.BudgetExceeded(f"{self.source}: not cached and paid calls are off")
        _guard_live_call()
        answer = self.live(payload)
        if "error" not in answer:
            stored = json.dumps(answer)
            with self._lock:
                self._db.execute("INSERT OR REPLACE INTO calls VALUES (?, ?)", (key, stored))
                self._db.commit()
        self._measure(payload, answer, cached=False)
        return answer

    def _measure(self, payload: dict[str, Any], answer: dict[str, Any], cached: bool) -> None:
        usage = answer.get("usage") or {}
        cost = float(usage.get("cost") or 0.0)
        model = str(payload.get("model"))
        prompt = int(usage.get("prompt_tokens") or 0)
        completion = int(usage.get("completion_tokens") or 0)
        meter.current().add(model, prompt, completion, cost, cached)
        if not cached:
            row = {"source": self.source, "model": model, "prompt_tokens": prompt}
            costlog.record({**row, "completion_tokens": completion, "cost_usd": cost})


def plantdocs_chat_transport(allow_paid: bool) -> CachedTransport:
    """A plantdocs `Client` szállítója."""
    load_env()
    path = CACHE_DIR / "plantdocs.sqlite"
    return CachedTransport(pd_openrouter.http_transport, "plantdocs-chat", allow_paid, path)


def plantdocs_embed_transport(allow_paid: bool) -> CachedTransport:
    """A plantdocs `Embedder` szállítója."""
    load_env()
    path = CACHE_DIR / "plantdocs-embeddings.sqlite"
    return CachedTransport(pd_embeddings.http_embed, "plantdocs-embed", allow_paid, path)
