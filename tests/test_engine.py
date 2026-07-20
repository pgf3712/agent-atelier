from __future__ import annotations

import unittest

from agent_atelier.domain import ActionKind, AgentAction, Budget, RunStatus
from agent_atelier.engine import run_agent
from agent_atelier.provider import SimulatedProvider


class UnknownToolProvider:
    def next_action(self, state):  # noqa: ANN001
        return AgentAction(
            kind=ActionKind.CALL_TOOL,
            rationale="Attempt a tool outside the allowlist.",
            tool_name="read_entire_computer",
            arguments={},
        )


class InvalidCitationProvider:
    def next_action(self, state):  # noqa: ANN001
        if not state.evidence:
            return AgentAction(
                kind=ActionKind.CALL_TOOL,
                rationale="Get evidence.",
                tool_name="search_local_corpus",
                arguments={"query": "agent safety budgets"},
            )
        return AgentAction(
            kind=ActionKind.FINAL_ANSWER,
            rationale="Try to cite evidence that was never returned.",
            answer="Unsupported answer",
            citations=("E-999",),
        )


class AdvancingClock:
    def __init__(self, milliseconds_per_read: int) -> None:
        self.value = 0.0
        self.increment = milliseconds_per_read / 1_000

    def __call__(self) -> float:
        current = self.value
        self.value += self.increment
        return current


class EngineTests(unittest.TestCase):
    def test_simulated_provider_completes_with_real_evidence_ids(self) -> None:
        state = run_agent("How do agent budgets improve safety?", SimulatedProvider())

        self.assertEqual(state.status, RunStatus.COMPLETED)
        self.assertTrue(state.answer)
        self.assertEqual(set(state.citations), {item.evidence_id for item in state.evidence})
        self.assertEqual(state.tool_calls, 1)
        self.assertEqual(state.events[-1].event_type, "run.completed")

    def test_no_matching_evidence_is_reported_honestly(self) -> None:
        state = run_agent("What is the weather on Neptune?", SimulatedProvider())

        self.assertEqual(state.status, RunStatus.INSUFFICIENT_EVIDENCE)
        self.assertIsNone(state.answer)

    def test_zero_tool_budget_stops_before_execution(self) -> None:
        state = run_agent(
            "How do agent budgets improve safety?",
            SimulatedProvider(),
            Budget(max_steps=3, max_tool_calls=0),
        )

        self.assertEqual(state.status, RunStatus.BUDGET_EXHAUSTED)
        self.assertEqual(state.tool_calls, 0)

    def test_unknown_tool_is_blocked(self) -> None:
        state = run_agent("Find a file", UnknownToolProvider())

        self.assertEqual(state.status, RunStatus.BLOCKED)
        self.assertEqual(state.events[-1].event_type, "tool.failed")

    def test_invented_citation_is_blocked(self) -> None:
        state = run_agent("Tell me about agent safety", InvalidCitationProvider())

        self.assertEqual(state.status, RunStatus.BLOCKED)
        self.assertIsNone(state.answer)
        self.assertEqual(state.events[-1].event_type, "policy.blocked")

    def test_wall_clock_budget_stops_before_provider_action(self) -> None:
        state = run_agent(
            "How do agent budgets improve safety?",
            SimulatedProvider(),
            Budget(max_steps=6, max_tool_calls=3, max_duration_ms=5),
            clock=AdvancingClock(milliseconds_per_read=6),
        )

        self.assertEqual(state.status, RunStatus.BUDGET_EXHAUSTED)
        self.assertEqual(state.steps, 0)
        self.assertEqual(state.events[-1].payload["budget"], "duration_ms")
        self.assertGreaterEqual(state.duration_ms, 5)

    def test_wall_clock_budget_must_be_positive(self) -> None:
        with self.assertRaises(ValueError):
            Budget(max_duration_ms=0)


if __name__ == "__main__":
    unittest.main()
