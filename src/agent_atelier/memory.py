"""Small in-memory teaching store separating run state, context and memory."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SessionMemory:
    _facts: dict[str, list[str]] = field(default_factory=dict)

    def remember(self, session_id: str, fact: str) -> tuple[str, ...]:
        session = _normalize_session(session_id)
        normalized = fact.strip()
        if not normalized:
            raise ValueError("Memory fact must not be empty.")
        if len(normalized) > 200:
            raise ValueError("Memory fact must be 200 characters or fewer.")
        facts = self._facts.setdefault(session, [])
        if normalized not in facts:
            facts.append(normalized)
        return tuple(facts)

    def recall(self, session_id: str) -> tuple[str, ...]:
        return tuple(self._facts.get(_normalize_session(session_id), ()))

    def clear(self, session_id: str) -> None:
        self._facts.pop(_normalize_session(session_id), None)


def build_context_snapshot(
    *, question: str, run_step: int, evidence_ids: list[str], remembered_facts: tuple[str, ...]
) -> dict[str, object]:
    return {
        "current_question": question.strip(),
        "current_step": run_step,
        "evidence_ids": list(evidence_ids),
        "remembered_facts": list(remembered_facts),
    }


def _normalize_session(session_id: str) -> str:
    normalized = session_id.strip()
    if not normalized:
        raise ValueError("Session identifier must not be empty.")
    if len(normalized) > 64:
        raise ValueError("Session identifier must be 64 characters or fewer.")
    return normalized
