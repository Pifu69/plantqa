"""A nem helyes válaszok fajtái egy mérésben: `uv run python scripts/failure_kinds.py EXP-060 a`.

Családonként és párosításonként megszámolja, hány nem helyes válasz volt „nincs benne” jelzés
(`not_present`), üres válasz (lépéskorlát, időtúllépés, feldolgozási hiba) vagy rossz tartalom.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def kinds(exp: str, family: str | None) -> dict[tuple[str, str], Counter[str]]:
    """Párosításonként a nem helyes válaszok fajtái."""
    out: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for line in (ROOT / "runs" / exp / "scored.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if family and row["family"] != family or row["score"]["verdict"] == "correct":
            continue
        final = row["answer"].get("final") or {}
        kind = "not_present" if final.get("not_present") else "empty" if not final else "content"
        out[(row["method"], row["model"])][kind] += 1
    return out


if __name__ == "__main__":
    exp_id, fam = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
    for key, counter in sorted(kinds(exp_id, fam).items()):
        print(exp_id, fam or "all", *key, dict(counter))
