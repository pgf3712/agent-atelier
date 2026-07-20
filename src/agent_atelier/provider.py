"""Provider protocol and deterministic offline teaching provider."""

from __future__ import annotations

from typing import Protocol

from agent_atelier.domain import ActionKind, AgentAction, RunState


class ActionProvider(Protocol):
    def next_action(self, state: RunState) -> AgentAction: ...


class SimulatedProvider:
    """Choose predictable actions so the loop can be learned and tested for free."""

    def next_action(self, state: RunState) -> AgentAction:
        if not state.evidence:
            return AgentAction(
                kind=ActionKind.CALL_TOOL,
                rationale="Search the permitted local corpus before making a claim.",
                tool_name="search_local_corpus",
                arguments={"query": state.question},
            )
        citations = tuple(item.evidence_id for item in state.evidence)
        findings = " ".join(item.content for item in state.evidence)
        return AgentAction(
            kind=ActionKind.FINAL_ANSWER,
            rationale="The available evidence is sufficient for a short, scoped brief.",
            answer=findings,
            citations=citations,
        )


class RepeatingProvider:
    """Test provider that deliberately repeats a call."""

    def next_action(self, state: RunState) -> AgentAction:
        return AgentAction(
            kind=ActionKind.CALL_TOOL,
            rationale="Repeat for loop-detection demonstration.",
            tool_name="search_local_corpus",
            arguments={"query": "no-match"},
        )
