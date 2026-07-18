# ADR 0008: Abstract usage units for the simulated provider

## Context

The offline provider returns no vendor token counts or prices. Fabricated dollar figures would mislead learners.

## Decision

The tutorial uses documented abstract units derived from character counts and tool calls. Latency has a separate millisecond budget.

## Alternatives

- Show fake token and dollar values.
- Omit resource accounting until a real provider exists.
- Combine all resource limits into one score.

## Consequences

The mechanism is teachable and deterministic without claiming financial accuracy. Real adapters must report their own usage and pricing assumptions.
