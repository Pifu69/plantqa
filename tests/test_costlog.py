import json
from pathlib import Path

import pytest

from plantqa import costlog


def test_spent_and_remaining(tmp_path: Path) -> None:
    ledger = tmp_path / "k.jsonl"
    costlog.record({"source": "x", "cost_usd": 1.5}, ledger)
    costlog.record({"source": "y", "cost_usd": 0.25}, ledger)
    assert costlog.spent_usd(ledger) == pytest.approx(1.75)
    assert costlog.remaining_usd(ledger) == pytest.approx(costlog.TOTAL_CAP_USD - 1.75)
    assert "time" in json.loads(ledger.read_text(encoding="utf-8").splitlines()[0])


def test_new_run_refused_at_stop(tmp_path: Path) -> None:
    ledger = tmp_path / "k.jsonl"
    costlog.record({"cost_usd": costlog.NEW_RUN_STOP_USD}, ledger)
    with pytest.raises(costlog.BudgetExceeded):
        costlog.check_new_run(ledger)


def test_empty_ledger(tmp_path: Path) -> None:
    assert costlog.spent_usd(tmp_path / "none.jsonl") == 0.0
