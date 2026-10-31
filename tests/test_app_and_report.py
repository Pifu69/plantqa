from __future__ import annotations

import json

from fastapi.testclient import TestClient

from plantqa.app.server import app
from plantqa.eval.report import summarize
from plantqa.questions.build import OUT_DIR


def test_config_and_examples() -> None:
    client = TestClient(app)
    config = client.get("/api/config").json()
    assert config["models"]["glm"] == "z-ai/glm-5.3-flash"
    assert config["tags"]["P-1-1"] == "gorman-rupp-0700286"
    examples = client.get("/api/examples").json()
    assert len(examples) == 20
    assert {e["family"] for e in examples} == {"a", "b", "c", "d"}


def test_unknown_method_and_document_are_refused() -> None:
    client = TestClient(app)
    assert client.post("/api/ask", json={"question": "x", "method": "M9"}).status_code == 400
    assert client.get("/api/datasheets/nope/pdf").status_code == 404


def _row(verdict: str, latency: float) -> dict[str, object]:
    usage = {"prompt_tokens": 10, "completion_tokens": 2, "cost_usd": 0.5, "spent_usd": 0.1}
    answer = {"usage": usage, "latency_s": latency}
    score = {"verdict": verdict}
    return {"method": "M1", "model": "glm", "split": "dev", "answer": answer, "score": score}


def test_summarize_counts_and_accuracy() -> None:
    out = summarize("EXP-X", [_row("correct", 1.0), _row("wrong", 3.0), _row("correct", 2.0)])
    assert (out["n"], out["correct"], out["wrong"]) == (3, 2, 1)
    assert out["accuracy"] == round(2 / 3, 4)
    assert out["cost_usd"] == 1.5 and out["latency_median_s"] == 2.0


def test_question_sets_have_the_planned_shape() -> None:
    for split, per_family in (("dev", 5), ("test", 10)):
        rows = [json.loads(x) for x in (OUT_DIR / f"{split}.jsonl").read_text("utf-8").splitlines()]
        for family in "abcd":
            assert sum(r["family"] == family for r in rows) == per_family
