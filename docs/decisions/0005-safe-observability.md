# ADR 0005: Allowlisted public events with redaction

## Context

Debugging needs execution facts, but raw provider/tool data may contain secrets, personal information or private reasoning.

## Decision

Only allowlisted, namespaced event types enter the public timeline. Payloads pass through deterministic recursive redaction and carry a schema version. Private-reasoning event categories are rejected.

## Alternatives

- Log complete prompts and model traces.
- Disable observability entirely.
- Rely on each tool to redact itself.

## Consequences

The timeline is safer and stable enough for the UI, but new event types require an explicit policy decision and tests.
