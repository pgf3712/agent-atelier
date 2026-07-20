"""Optional OpenAI Responses adapter kept outside the zero-dependency learning core."""

from __future__ import annotations

import importlib.util
import json
import os
from typing import Any

from agent_atelier.domain import ActionKind, AgentAction, RunState
from agent_atelier.provider import ActionProvider, SimulatedProvider


class ProviderConfigurationError(RuntimeError):
    """Raised before a paid request when optional provider configuration is incomplete."""


SEARCH_TOOL = {
    "type": "function",
    "name": "search_local_corpus",
    "description": "Search the bundled, trusted teaching corpus for evidence.",
    "parameters": {
        "type": "object",
        "properties": {"query": {"type": "string", "minLength": 1}},
        "required": ["query"],
        "additionalProperties": False,
    },
    "strict": True,
}


class OpenAIResponsesProvider:
    """Translate Responses API function calls into the repository's provider-neutral actions."""

    def __init__(self, *, model: str, client: Any | None = None) -> None:
        if not model.strip():
            raise ProviderConfigurationError("AGENT_ATELIER_MODEL must name an enabled model.")
        if client is None:
            try:
                from openai import OpenAI
            except ImportError as exc:  # pragma: no cover - depends on optional installation
                raise ProviderConfigurationError(
                    "Install the optional provider with: python -m pip install -e .[real]"
                ) from exc
            client = OpenAI()
        self.client = client
        self.model = model.strip()
        self._response_id: str | None = None
        self._call_id: str | None = None

    def next_action(self, state: RunState) -> AgentAction:
        if not state.evidence:
            response = self.client.responses.create(
                model=self.model,
                instructions=(
                    "You are the proposal layer inside a bounded educational agent. "
                    "Request search_local_corpus once. Never invent evidence or system capabilities."
                ),
                input=state.question,
                tools=[SEARCH_TOOL],
                tool_choice="required",
            )
            tool_call = next(
                (item for item in response.output if item.type == "function_call"), None
            )
            if tool_call is None or tool_call.name != "search_local_corpus":
                return AgentAction(
                    kind=ActionKind.INSUFFICIENT_EVIDENCE,
                    rationale="The real provider did not propose the required allowed search.",
                )
            try:
                arguments = json.loads(tool_call.arguments)
            except (TypeError, json.JSONDecodeError) as exc:
                raise ProviderConfigurationError("Provider returned invalid tool JSON.") from exc
            self._response_id = response.id
            self._call_id = tool_call.call_id
            return AgentAction(
                kind=ActionKind.CALL_TOOL,
                rationale="The real provider proposed the allowlisted local evidence search.",
                tool_name=tool_call.name,
                arguments=arguments,
            )

        if not self._response_id or not self._call_id:
            raise ProviderConfigurationError("Tool result cannot be resumed without its call ID.")
        evidence_payload = [
            {
                "evidence_id": item.evidence_id,
                "title": item.title,
                "content": item.content,
                "source": item.source,
            }
            for item in state.evidence
        ]
        response = self.client.responses.create(
            model=self.model,
            previous_response_id=self._response_id,
            instructions=(
                "Write a short research brief using only the function output. "
                "State limitations. Do not claim access to any other source."
            ),
            input=[
                {
                    "type": "function_call_output",
                    "call_id": self._call_id,
                    "output": json.dumps(evidence_payload, ensure_ascii=False),
                }
            ],
            tools=[SEARCH_TOOL],
        )
        answer = response.output_text.strip()
        if not answer:
            return AgentAction(
                kind=ActionKind.INSUFFICIENT_EVIDENCE,
                rationale="The real provider returned no final brief.",
            )
        return AgentAction(
            kind=ActionKind.FINAL_ANSWER,
            rationale="The real provider summarized the application-supplied evidence.",
            answer=answer,
            citations=tuple(item.evidence_id for item in state.evidence),
        )


def provider_status() -> dict[str, object]:
    """Return configuration facts without exposing an API key or its prefix."""

    return {
        "simulated_available": True,
        "openai_sdk_installed": importlib.util.find_spec("openai") is not None,
        "openai_key_configured": bool(os.environ.get("OPENAI_API_KEY", "").strip()),
        "openai_model_configured": bool(os.environ.get("AGENT_ATELIER_MODEL", "").strip()),
    }


def build_provider(name: str) -> ActionProvider:
    normalized = name.strip().lower()
    if normalized == "simulated":
        return SimulatedProvider()
    if normalized != "openai":
        raise ProviderConfigurationError(f"Unknown provider: {name}")
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        raise ProviderConfigurationError("OPENAI_API_KEY is not configured on the local server.")
    model = os.environ.get("AGENT_ATELIER_MODEL", "").strip()
    if not model:
        raise ProviderConfigurationError("AGENT_ATELIER_MODEL is not configured on the local server.")
    return OpenAIResponsesProvider(model=model)
