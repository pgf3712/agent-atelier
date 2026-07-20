"""Bounded orchestration loop owned by the application, not the provider."""

from __future__ import annotations

import json
from collections.abc import Callable
from time import monotonic

from agent_atelier.domain import ActionKind, Budget, RunState, RunStatus
from agent_atelier.provider import ActionProvider
from agent_atelier.tools import ToolError, execute_tool


def _fingerprint(action_kind: str, tool_name: str | None, arguments: dict[str, object]) -> str:
    return json.dumps([action_kind, tool_name, arguments], sort_keys=True)


def run_agent(
    question: str,
    provider: ActionProvider,
    budget: Budget | None = None,
    *,
    clock: Callable[[], float] = monotonic,
) -> RunState:
    normalized = question.strip()
    if not normalized:
        raise ValueError("Question must not be empty.")

    state = RunState(question=normalized, budget=budget or Budget())
    started_at = clock()

    def update_duration() -> None:
        state.duration_ms = max(0, int((clock() - started_at) * 1_000))

    def stop_if_timed_out() -> bool:
        update_duration()
        if state.duration_ms < state.budget.max_duration_ms:
            return False
        state.status = RunStatus.BUDGET_EXHAUSTED
        state.emit(
            "budget.exhausted",
            budget="duration_ms",
            elapsed_ms=state.duration_ms,
        )
        return True

    state.status = RunStatus.ACTING
    state.emit("run.started", question=normalized)

    while state.steps < state.budget.max_steps:
        if stop_if_timed_out():
            return state
        state.steps += 1
        action = provider.next_action(state)
        if stop_if_timed_out():
            return state
        state.emit(
            "action.proposed",
            kind=action.kind.value,
            rationale=action.rationale,
        )

        if action.kind == ActionKind.FINAL_ANSWER:
            known_ids = {item.evidence_id for item in state.evidence}
            if not action.answer or not set(action.citations).issubset(known_ids):
                state.status = RunStatus.BLOCKED
                state.emit("policy.blocked", reason="Answer or citations failed validation.")
                return state
            state.answer = action.answer
            state.citations = action.citations
            state.status = RunStatus.COMPLETED
            state.emit("run.completed", citations=list(action.citations))
            update_duration()
            return state

        if action.kind == ActionKind.INSUFFICIENT_EVIDENCE:
            state.status = RunStatus.INSUFFICIENT_EVIDENCE
            state.emit("run.insufficient_evidence")
            update_duration()
            return state

        if action.kind != ActionKind.CALL_TOOL or not action.tool_name:
            state.status = RunStatus.BLOCKED
            state.emit("policy.blocked", reason="Provider proposed an invalid action.")
            update_duration()
            return state

        fingerprint = _fingerprint(action.kind.value, action.tool_name, action.arguments)
        if fingerprint in state.seen_actions:
            state.status = RunStatus.BLOCKED
            state.emit("policy.blocked", reason="Repeated action detected.")
            update_duration()
            return state
        state.seen_actions.add(fingerprint)

        if state.tool_calls >= state.budget.max_tool_calls:
            state.status = RunStatus.BUDGET_EXHAUSTED
            state.emit("budget.exhausted", budget="tool_calls")
            update_duration()
            return state

        state.tool_calls += 1
        state.emit("tool.started", tool=action.tool_name)
        try:
            evidence = execute_tool(action.tool_name, action.arguments)
        except ToolError as exc:
            state.status = RunStatus.BLOCKED
            state.emit("tool.failed", tool=action.tool_name, error=str(exc))
            update_duration()
            return state
        if stop_if_timed_out():
            return state
        state.evidence.extend(evidence)
        state.emit(
            "tool.completed",
            tool=action.tool_name,
            evidence_ids=[item.evidence_id for item in evidence],
        )
        if not evidence:
            state.status = RunStatus.INSUFFICIENT_EVIDENCE
            state.emit("run.insufficient_evidence")
            update_duration()
            return state

    state.status = RunStatus.BUDGET_EXHAUSTED
    state.emit("budget.exhausted", budget="steps")
    update_duration()
    return state
