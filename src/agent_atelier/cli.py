"""Tiny CLI for demonstrating the offline loop."""

from __future__ import annotations

import argparse
import json
import os

from agent_atelier.engine import run_agent
from agent_atelier.real_provider import build_provider


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Agent Atelier's simulated agent.")
    parser.add_argument("question", nargs="?", default="How do agent budgets improve safety?")
    parser.add_argument(
        "--provider",
        choices=("simulated", "openai"),
        default=os.environ.get("AGENT_ATELIER_PROVIDER", "simulated"),
        help="Use the free simulator or an explicitly configured server-side adapter.",
    )
    args = parser.parse_args()
    state = run_agent(args.question, build_provider(args.provider))
    print(f"Status: {state.status.value}")
    print(f"Answer: {state.answer or 'No supported answer.'}")
    print(f"Citations: {', '.join(state.citations) or 'none'}")
    print("Events:")
    for event in state.events:
        print(json.dumps(event.__dict__, ensure_ascii=False))
    return 0 if state.answer else 1


if __name__ == "__main__":
    raise SystemExit(main())
