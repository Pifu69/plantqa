"""A demó képernyőképei: `python -m plantqa.app.screens` (a demónak futnia kell).

Minden kérdést előbb az API-n kérdez meg (a válasz így a cache-be kerül), majd a fej nélküli
Chrome-mal lefényképezi a `?q=…` paraméterrel megnyitott oldalt, amely betöltéskor felteszi a
kérdést. Kimenet: `figures/demo/NN-<család>-<módszer>.png` és `figures/demo/screens.csv`.
"""

from __future__ import annotations

import csv
import json
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

from plantqa.graph.sources import ROOT

BASE = "http://127.0.0.1:8010"
CHROME = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
OUT = ROOT / "figures" / "demo"
#: (család, kérdés, módszer, modell, válaszalak) — minden családból legalább egy.
SCREENS = [
    ("c", "Consider the transmitter that measures E-2-1. What is the lowest operating "
     "temperature you get with the BR6 option?", "M2", "glm", "FREE_TEXT"),
    ("a", "Trace the process flow path from CHV-1-2 to CHV-2-1. List every equipment item and "
     "valve in order.", "M1", "glm", "TAG_PATH"),
    ("b", "Regarding P-1-3 on the P&ID: What's the max allowable pressure in the casing? We might "
     "have a pressurized inlet.", "M1", "glm", "FREE_TEXT"),
    ("d", "Regarding GV-1-1 on the P&ID: Is it approved for drinking water, or for use in an "
     "explosive (Ex) area?", "M2", "glm", "FREE_TEXT"),
    ("e", "For each item that receives flow directly from P-2-1, what is its maximum allowable "
     "pressure according to its datasheet, and which of them has the lowest?", "M2", "glm",
     "FREE_TEXT"),
    ("a", "Which instruments measure E-2-1?", "M3", "glm", "TAG_SET"),
]  # fmt: skip


def ask(question: str, method: str, model: str, answer_type: str) -> dict[str, object]:
    """Egy kérdés az API-n (a válasz a cache-be kerül)."""
    body = {"question": question, "method": method, "model": model, "answer_type": answer_type}
    request = urllib.request.Request(
        f"{BASE}/api/ask",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        return dict(json.loads(response.read().decode("utf-8")))


def first_page(answer: dict[str, object]) -> str:
    """Az első adatlapi forrásoldal `doc:N` alakban (a bal oldalon ez jelenik meg), vagy üres."""
    for source in list(answer.get("sources") or []):  # type: ignore[call-overload]
        pages = list(source.get("pages") or [])
        if pages:
            return f"{source['document_id']}:{pages[0]}"
    return ""


def shoot(path: Path, question: str, method: str, model: str, answer_type: str, page: str) -> None:
    """Fej nélküli Chrome-képernyőkép a kérdést betöltéskor feltevő oldalról."""
    params = {"q": question, "method": method, "model": model, "type": answer_type}
    query = urllib.parse.urlencode({**params, "page": page} if page else params)
    command = [
        str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--window-size=1600,900", "--virtual-time-budget=20000",
        f"--screenshot={path}", f"{BASE}/?{query}",
    ]  # fmt: skip
    subprocess.run(command, check=True, capture_output=True, timeout=180)


def main() -> None:
    """Minden képernyőkép újragenerálása."""
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, (family, question, method, model, answer_type) in enumerate(SCREENS, start=1):
        answer = ask(question, method, model, answer_type)
        path = OUT / f"{index:02d}-{family}-{method}.png"
        shoot(path, question, method, model, answer_type, first_page(answer))
        route = " ".join(str(step) for step in list(answer.get("route") or []))  # type: ignore[call-overload]
        text = str(answer.get("text", ""))[:200]
        rows.append({"file": path.name, "family": family, "method": method, "model": model,
                     "question": question, "route": route, "answer_start": text})  # fmt: skip
        print(path.name, route)
    with (OUT / "screens.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
