"""Explicit, deterministic planning primitives for the teaching lab."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum


class StepStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


@dataclass
class PlanStep:
    step_id: str
    title: str
    success_condition: str
    status: StepStatus = StepStatus.PENDING


@dataclass
class ResearchPlan:
    goal: str
    steps: list[PlanStep]

    def activate_first(self) -> None:
        if self.steps and all(step.status == StepStatus.PENDING for step in self.steps):
            self.steps[0].status = StepStatus.ACTIVE

    def complete_active(self) -> None:
        active_index = next(
            (index for index, step in enumerate(self.steps) if step.status == StepStatus.ACTIVE),
            None,
        )
        if active_index is None:
            raise ValueError("Plan has no active step.")
        self.steps[active_index].status = StepStatus.COMPLETED
        if active_index + 1 < len(self.steps):
            self.steps[active_index + 1].status = StepStatus.ACTIVE

    @property
    def completed(self) -> bool:
        return bool(self.steps) and all(step.status == StepStatus.COMPLETED for step in self.steps)

    def as_dict(self) -> dict[str, object]:
        return {"goal": self.goal, "steps": [asdict(step) for step in self.steps], "completed": self.completed}


def create_research_plan(question: str, locale: str = "en") -> ResearchPlan:
    goal = question.strip()
    if not goal:
        raise ValueError("Planning goal must not be empty.")
    if len(goal) > 500:
        raise ValueError("Planning goal must be 500 characters or fewer.")
    step_copy = (
        (
            ("Aclarar la pregunta", "El alcance y los términos clave son explícitos."),
            ("Reunir evidencia local", "Existe al menos una evidencia pertinente o un resultado vacío honesto."),
            ("Comprobar la evidencia", "Cada afirmación corresponde a un identificador de evidencia conocido."),
            ("Redactar el informe", "Los hallazgos y las limitaciones aparecen separados."),
        )
        if locale == "es"
        else (
            ("Clarify the question", "Scope and key terms are explicit."),
            ("Gather local evidence", "At least one relevant evidence item or an honest empty result."),
            ("Check evidence", "Every claim maps to a known evidence identifier."),
            ("Write the brief", "Findings and limitations are separated."),
        )
    )
    plan = ResearchPlan(
        goal=goal,
        steps=[
            PlanStep(f"P-{index:02}", title, condition)
            for index, (title, condition) in enumerate(step_copy, start=1)
        ],
    )
    plan.activate_first()
    return plan
