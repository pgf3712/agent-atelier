# ADR 0007: Scoped, single-use approvals

## Context

A generic confirmation can be replayed or applied to a more dangerous action than the user saw.

## Decision

Approval binds action name and canonical argument digest to a single-use capability. Denial creates no capability; consumption invalidates it.

## Alternatives

- Boolean `approved=true` in session state.
- Approve a tool category for the whole session.
- Execute first and ask afterwards.

## Consequences

Approval is explicit and replay-resistant in the teaching model. Production expiry, identity and durable audit storage remain future adapter concerns.
