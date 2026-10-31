"""Közös költségnapló (`logs/koltseg.jsonl`) és a teljes keretre vonatkozó spend guard.

Minden fizetős hívás egy sort kap a naplóban. A keret (PROMPT 2. szabály): összesen 20 USD;
18 USD felett új mérés nem indul, csak a cache-ből lehet dolgozni.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "logs" / "koltseg.jsonl"
TOTAL_CAP_USD = 20.0
NEW_RUN_STOP_USD = 18.0
AZURE_LAYOUT_USD_PER_PAGE = 0.01
"""Az Azure DI prebuilt-layout listaára (10 USD / 1000 oldal), ahogy a plantdocs EXP-0038 számol."""


class BudgetExceeded(Exception):
    """A közös keret elfogyott: új fizetős futás nem indulhat."""


def record(row: dict[str, Any], ledger: Path = LEDGER) -> None:
    """Egy fizetős hívás sorának hozzáfűzése a naplóhoz (időbélyeggel)."""
    ledger.parent.mkdir(parents=True, exist_ok=True)
    full = {"time": datetime.now(UTC).isoformat(timespec="seconds"), **row}
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(full, ensure_ascii=False) + "\n")


def spent_usd(ledger: Path = LEDGER) -> float:
    """Az eddig elköltött összeg a napló alapján."""
    if not ledger.exists():
        return 0.0
    lines = ledger.read_text(encoding="utf-8").splitlines()
    return sum(float(json.loads(line).get("cost_usd") or 0.0) for line in lines if line.strip())


def remaining_usd(ledger: Path = LEDGER) -> float:
    """A teljes keretből még elkölthető összeg."""
    return max(0.0, TOTAL_CAP_USD - spent_usd(ledger))


def check_new_run(ledger: Path = LEDGER) -> None:
    """Új fizetős mérés előtti ellenőrzés: 18 USD felett megtagadja."""
    spent = spent_usd(ledger)
    if spent >= NEW_RUN_STOP_USD:
        message = f"spent {spent:.4f} USD >= {NEW_RUN_STOP_USD} USD: cache-only from now"
        raise BudgetExceeded(message)


def record_azure(pdf: Path, tag: str) -> float:
    """Egy Azure DI elemzés listaáras költségének naplózása; a visszatérési érték a költség."""
    pages = int(pymupdf.open(pdf).page_count)  # type: ignore[no-untyped-call]
    cost = float(round(pages * AZURE_LAYOUT_USD_PER_PAGE, 4))
    record(
        {
            "source": "azure-di",
            "tag": tag,
            "model": "prebuilt-layout",
            "pages": pages,
            "cost_usd": cost,
            "cost_basis": "list price 10 USD / 1000 pages (estimate, not billed amount)",
        }
    )
    return cost


def main() -> None:
    """Parancssor: `azure` (Azure-költség naplózása) vagy `status` (eddigi költés)."""
    parser = argparse.ArgumentParser(description="Shared cost ledger")
    sub = parser.add_subparsers(dest="command", required=True)
    azure = sub.add_parser("azure")
    azure.add_argument("--pdf", type=Path, required=True)
    azure.add_argument("--tag", required=True)
    sub.add_parser("status")
    args = parser.parse_args()
    if args.command == "azure":
        print(f"azure cost logged: {record_azure(args.pdf, args.tag):.4f} USD")
        return
    print(f"spent {spent_usd():.4f} USD, remaining {remaining_usd():.4f} USD of {TOTAL_CAP_USD}")


if __name__ == "__main__":
    main()
