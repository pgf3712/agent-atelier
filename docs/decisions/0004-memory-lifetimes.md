# ADR 0004: Separate run state, context and memory lifetimes

## Context

Calling every retained value “memory” leads to unbounded prompts, cross-session leaks and unclear deletion.

## Decision

Run state, context snapshots and session memory have separate contracts. The teaching store is in memory, scoped by explicit session ID, and retains only deliberate facts.

## Alternatives

- One global object for every kind of state.
- Persist the complete conversation automatically.
- Add a database before teaching the lifetime model.

## Advantages

- Lifetimes and deletion are visible.
- Session isolation is directly testable.
- The mechanism needs no infrastructure.

## Disadvantages

- Memory disappears when the preview server stops.
- The store has no multi-process guarantees.

## Consequences

A durable adapter may replace it later, but must preserve isolation, explicit writes, bounded recall and deletion semantics.
