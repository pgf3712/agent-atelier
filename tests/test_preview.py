from __future__ import annotations

import unittest

from agent_atelier.preview import _run_payload, _validate_bind_target
from agent_atelier.tools import ToolError, execute_tool


class PreviewApiTests(unittest.TestCase):
    def test_payload_runs_real_engine(self) -> None:
        result = _run_payload(
            {
                "question": "How do agent budgets improve safety?",
                "max_steps": 6,
                "max_tool_calls": 3,
            }
        )

        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["tool_calls"], 1)
        self.assertTrue(result["evidence"])
        self.assertEqual(result["events"][-1]["event_type"], "run.completed")

    def test_payload_respects_zero_tool_budget(self) -> None:
        result = _run_payload(
            {
                "question": "How do agent budgets improve safety?",
                "max_steps": 6,
                "max_tool_calls": 0,
            }
        )

        self.assertEqual(result["status"], "budget_exhausted")
        self.assertEqual(result["tool_calls"], 0)

    def test_payload_rejects_invalid_question(self) -> None:
        with self.assertRaises(ValueError):
            _run_payload({"question": "", "max_steps": 6, "max_tool_calls": 3})

    def test_payload_rejects_unknown_provider(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "Unknown provider"):
            _run_payload({"question": "Question", "provider": "mystery"})

    def test_chapter_two_valid_tool_case_executes(self) -> None:
        evidence = execute_tool("search_local_corpus", {"query": "agent budgets"})

        self.assertTrue(evidence)

    def test_chapter_two_invalid_tool_case_is_blocked(self) -> None:
        with self.assertRaises(ToolError):
            execute_tool(
                "search_local_corpus",
                {"query": "agent budgets", "path": "C:/Users"},
            )

    def test_preview_module_exposes_later_chapter_components(self) -> None:
        from agent_atelier.approvals import ApprovalStore
        from agent_atelier.costs import CostPolicy, estimate_usage

        approval = ApprovalStore().propose("export_brief", {"format": "markdown"}, "Export")
        usage = estimate_usage(input_characters=100, output_characters=50, tool_calls=1, latency_ms=500, policy=CostPolicy(10, 1000))
        self.assertEqual(approval.status.value, "pending")
        self.assertTrue(usage.within_cost_budget)

    def test_preview_binds_to_loopback_by_default(self) -> None:
        for host in ("127.0.0.1", "localhost", "::1"):
            _validate_bind_target(host, allow_remote=False)

    def test_preview_rejects_remote_binding_without_explicit_opt_in(self) -> None:
        with self.assertRaisesRegex(ValueError, "Refusing to expose"):
            _validate_bind_target("0.0.0.0", allow_remote=False)

        _validate_bind_target("0.0.0.0", allow_remote=True)


if __name__ == "__main__":
    unittest.main()
