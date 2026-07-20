"""Integrated offline application service used by Chapter 10."""

from __future__ import annotations

from dataclasses import asdict

from agent_atelier.costs import CostPolicy, estimate_usage
from agent_atelier.domain import Budget, RunStatus
from agent_atelier.engine import run_agent
from agent_atelier.evaluation import pass_rate, run_evaluation
from agent_atelier.planning import create_research_plan
from agent_atelier.provider import ActionProvider, SimulatedProvider


def run_research_brief(
    question: str, *, max_steps: int = 6, max_tool_calls: int = 3, max_cost_units: int = 30,
    locale: str = "en", provider: ActionProvider | None = None,
) -> dict[str, object]:
    plan = create_research_plan(question, locale)
    plan.complete_active()  # question clarified by validated input

    state = run_agent(question, provider or SimulatedProvider(), Budget(max_steps, max_tool_calls))
    if state.tool_calls > 0:
        plan.complete_active()  # local corpus search completed, even when it found no match
    if state.status == RunStatus.COMPLETED:
        plan.complete_active()  # citation integrity was checked by the engine
        plan.complete_active()  # the final brief was accepted

    answer = state.answer or ""
    usage = estimate_usage(
        input_characters=len(question), output_characters=len(answer),
        tool_calls=state.tool_calls, latency_ms=len(state.events) * 120,
        policy=CostPolicy(max_cost_units=max_cost_units, max_latency_ms=2_000),
    )
    evaluation = run_evaluation()
    return {
        "question": state.question,
        "status": state.status.value,
        "plan": plan.as_dict(),
        "brief": {
            "answer": state.answer,
            "citations": list(state.citations),
            "limitations": (
                ["El resultado utiliza únicamente el corpus didáctico local incluido."]
                if locale == "es" and state.answer
                else ["El corpus incluido no contenía suficiente evidencia pertinente."]
                if locale == "es"
                else ["The result uses only the bundled local teaching corpus."]
                if state.answer
                else ["The bundled corpus did not contain enough relevant evidence."]
            ),
        },
        "evidence": [asdict(item) for item in state.evidence],
        "events": [asdict(item) for item in state.events],
        "usage": asdict(usage),
        "evaluation": {
            "pass_rate": pass_rate(evaluation),
            "passed": sum(item.passed for item in evaluation),
            "total": len(evaluation),
        },
    }
