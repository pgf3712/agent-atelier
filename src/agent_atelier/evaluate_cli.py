"""Command-line report for deterministic evaluation scenarios."""

from __future__ import annotations

from agent_atelier.evaluation import pass_rate, run_evaluation


def main() -> int:
    results = run_evaluation()
    for result in results:
        marker = "PASS" if result.passed else "FAIL"
        print(f"[{marker}] {result.scenario_id}: {', '.join(result.checks)}")
    print(f"Pass rate: {pass_rate(results):.0%} ({sum(r.passed for r in results)}/{len(results)})")
    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
