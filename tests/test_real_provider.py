from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from agent_atelier.engine import run_agent
from agent_atelier.real_provider import (
    OpenAIResponsesProvider,
    ProviderConfigurationError,
    build_provider,
    provider_status,
)


class FakeResponses:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> SimpleNamespace:
        self.calls.append(kwargs)
        if len(self.calls) == 1:
            tool_call = SimpleNamespace(
                type="function_call",
                name="search_local_corpus",
                arguments='{"query": "agent budgets"}',
                call_id="call-1",
            )
            return SimpleNamespace(id="response-1", output=[tool_call], output_text="")
        return SimpleNamespace(
            id="response-2",
            output=[],
            output_text="Budgets keep execution bounded and observable.",
        )


class RealProviderAdapterTests(unittest.TestCase):
    def test_responses_function_call_is_translated_into_harness_actions(self) -> None:
        responses = FakeResponses()
        client = SimpleNamespace(responses=responses)
        provider = OpenAIResponsesProvider(model="configured-model", client=client)

        state = run_agent("How do agent budgets improve safety?", provider)

        self.assertEqual(state.status.value, "completed")
        self.assertEqual(state.tool_calls, 1)
        self.assertEqual(state.citations, tuple(item.evidence_id for item in state.evidence))
        self.assertIn("E-001", state.citations)
        self.assertEqual(responses.calls[0]["tool_choice"], "required")
        self.assertEqual(responses.calls[1]["previous_response_id"], "response-1")
        self.assertEqual(responses.calls[1]["input"][0]["type"], "function_call_output")

    def test_status_never_returns_the_key_value(self) -> None:
        with patch.dict(
            "os.environ",
            {"OPENAI_API_KEY": "secret-value", "AGENT_ATELIER_MODEL": "configured-model"},
            clear=True,
        ):
            status = provider_status()

        self.assertTrue(status["openai_key_configured"])
        self.assertNotIn("secret-value", repr(status))

    def test_openai_provider_requires_server_side_configuration(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ProviderConfigurationError, "OPENAI_API_KEY"):
                build_provider("openai")

    def test_openai_provider_uses_environment_configuration_only(self) -> None:
        with patch("agent_atelier.real_provider.OpenAIResponsesProvider") as provider_class:
            with patch.dict(
                "os.environ",
                {"OPENAI_API_KEY": "environment-key", "AGENT_ATELIER_MODEL": "configured-model"},
                clear=True,
            ):
                build_provider("openai")

        provider_class.assert_called_once_with(model="configured-model")


if __name__ == "__main__":
    unittest.main()
