"""Safe public-event projection and deterministic redaction."""

from __future__ import annotations

import re
from typing import Any

SECRET_KEYS = {"api_key", "authorization", "password", "secret", "token"}
SECRET_PATTERNS = (
    re.compile(r"(?i)(bearer\s+)[a-z0-9._-]+"),
    re.compile(r"(?i)(api[_-]?key\s*[=:]\s*)[^\s,;]+"),
)


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]" if str(key).lower() in SECRET_KEYS else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, tuple):
        return [redact(item) for item in value]
    if isinstance(value, str):
        result = value
        for pattern in SECRET_PATTERNS:
            result = pattern.sub(r"\1[REDACTED]", result)
        return result
    return value


def public_event(event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not event_type or "." not in event_type:
        raise ValueError("Public event type must use a namespaced form.")
    allowed = {
        "action.proposed", "tool.started", "tool.completed", "tool.failed",
        "policy.blocked", "budget.exhausted", "run.completed", "run.failed",
    }
    if event_type not in allowed:
        raise ValueError(f"Event type '{event_type}' is not public.")
    return {"schema_version": "1.0", "event_type": event_type, "payload": redact(payload)}
