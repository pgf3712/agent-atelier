"""Small domain model for safe, observable agent runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class RunStatus(StrEnum):
    CREATED = "created"
    ACTING = "acting"
    COMPLETED = "completed"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    BUDGET_EXHAUSTED = "budget_exhausted"
    BLOCKED = "blocked"
    FAILED = "failed"


class ActionKind(StrEnum):
    CALL_TOOL = "call_tool"
    FINAL_ANSWER = "final_answer"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


@dataclass(frozen=True)
class Budget:
    max_steps: int = 6
    max_tool_calls: int = 3
    max_duration_ms: int = 5_000

    def __post_init__(self) -> None:
        if self.max_steps < 1 or self.max_tool_calls < 0 or self.max_duration_ms < 1:
            raise ValueError(
                "Budget values must allow one step, non-negative tool calls and positive time."
            )


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    title: str
    content: str
    source: str


@dataclass(frozen=True)
class AgentAction:
    kind: ActionKind
    rationale: str
    tool_name: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)
    answer: str | None = None
    citations: tuple[str, ...] = ()


@dataclass(frozen=True)
class RunEvent:
    sequence: int
    event_type: str
    payload: dict[str, Any]
    schema_version: str = "1.0"


@dataclass
class RunState:
    question: str
    budget: Budget
    status: RunStatus = RunStatus.CREATED
    steps: int = 0
    tool_calls: int = 0
    duration_ms: int = 0
    evidence: list[EvidenceItem] = field(default_factory=list)
    events: list[RunEvent] = field(default_factory=list)
    answer: str | None = None
    citations: tuple[str, ...] = ()
    seen_actions: set[str] = field(default_factory=set)

    def emit(self, event_type: str, **payload: Any) -> None:
        self.events.append(RunEvent(len(self.events) + 1, event_type, payload))
