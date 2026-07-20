from __future__ import annotations

import unittest

from agent_atelier.final_app import run_research_brief


class FinalApplicationTests(unittest.TestCase):
    def test_supported_question_integrates_all_layers(self) -> None:
        result = run_research_brief("How do agent budgets improve safety?")
        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["plan"]["completed"])
        self.assertTrue(result["brief"]["citations"])
        self.assertTrue(result["evidence"])
        self.assertTrue(result["events"])
        self.assertEqual(result["evaluation"]["pass_rate"], 1.0)

    def test_unsupported_question_keeps_plan_honest(self) -> None:
        result = run_research_brief("What is the weather on Neptune?")
        self.assertEqual(result["status"], "insufficient_evidence")
        self.assertFalse(result["plan"]["completed"])
        self.assertIsNone(result["brief"]["answer"])
        self.assertTrue(result["brief"]["limitations"])

    def test_zero_tool_budget_produces_no_evidence(self) -> None:
        result = run_research_brief(
            "How do agent budgets improve safety?", max_tool_calls=0
        )
        self.assertEqual(result["status"], "budget_exhausted")
        self.assertEqual(result["evidence"], [])

    def test_spanish_run_localizes_plan_evidence_and_limitations(self) -> None:
        result = run_research_brief(
            "¿Cómo mejoran la seguridad los presupuestos de un agente?", locale="es"
        )

        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["plan"]["steps"][0]["title"], "Aclarar la pregunta")
        self.assertIn("presupuestos", result["evidence"][0]["content"])
        self.assertIn("corpus didáctico", result["brief"]["limitations"][0])


if __name__ == "__main__":
    unittest.main()
