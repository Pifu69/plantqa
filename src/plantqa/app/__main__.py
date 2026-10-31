"""Indítás: `uv run python -m plantqa.app` (http://127.0.0.1:8010)."""

from __future__ import annotations

import argparse

import uvicorn


def main() -> None:
    """A webszerver indítása."""
    parser = argparse.ArgumentParser(description="plantqa demo")
    parser.add_argument("--port", type=int, default=8010)
    parser.add_argument("--replay-only", action="store_true", help="answer from the cache only")
    args = parser.parse_args()
    from plantqa.app import server

    server.ALLOW_PAID = not args.replay_only
    uvicorn.run(server.app, host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
