from __future__ import annotations

import unittest

from agent_atelier.tools import ToolError, execute_tool, public_tool_catalog


class ToolContractTests(unittest.TestCase):
    def test_valid_arguments_are_normalized(self) -> None:
        evidence = execute_tool("search_local_corpus", {"query": "  agent budgets  "})

        self.assertTrue(evidence)

    def test_spanish_query_returns_equivalent_local_evidence_in_spanish(self) -> None:
        evidence = execute_tool(
            "search_local_corpus",
            {"query": "¿Cómo mejoran los presupuestos la seguridad de un agente?"},
        )

        self.assertEqual(evidence[0].evidence_id, "E-001")
        self.assertIn("límites", evidence[0].content)

    def test_missing_required_argument_is_rejected(self) -> None:
        with self.assertRaisesRegex(ToolError, "Missing required argument 'query'"):
            execute_tool("search_local_corpus", {})

    def test_wrong_argument_type_is_rejected(self) -> None:
        with self.assertRaisesRegex(ToolError, "must be str"):
            execute_tool("search_local_corpus", {"query": 42})

    def test_empty_string_is_rejected(self) -> None:
        with self.assertRaisesRegex(ToolError, "at least 1 character"):
            execute_tool("search_local_corpus", {"query": "   "})

    def test_unexpected_argument_is_rejected(self) -> None:
        with self.assertRaisesRegex(ToolError, "Unexpected argument"):
            execute_tool(
                "search_local_corpus",
                {"query": "agent budgets", "path": "C:/Users"},
            )

    def test_unknown_tool_is_rejected_before_argument_validation(self) -> None:
        with self.assertRaisesRegex(ToolError, "is not allowed"):
            execute_tool("shell", {"command": "whoami"})

    def test_public_catalog_contains_no_callable_objects(self) -> None:
        catalog = public_tool_catalog()

        self.assertEqual(catalog[0]["name"], "search_local_corpus")
        self.assertEqual(catalog[0]["arguments"]["query"]["type"], "str")
        self.assertNotIn("handler", catalog[0])


if __name__ == "__main__":
    unittest.main()
