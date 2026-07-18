# ADR 0002: Deterministic evaluation before model-based judging

## Context

Agent behavior can fail at tool selection, validation, stopping, citation integrity and permissions. A vague quality score would hide these distinct failures and make CI unreliable.

## Decision

The first evaluation suite uses deterministic providers, exact expected terminal states and computable checks. Essential scenarios run without a network or API key.

## Alternatives

- Ask a hosted LLM to score every answer.
- Keep only ordinary unit tests around helper functions.
- Evaluate manually through the web interface.

## Advantages

- Reproducible and free in CI.
- Failures point to a specific safety contract.
- Interview claims can link to executable evidence.

## Disadvantages

- Deterministic scenarios do not measure the linguistic quality of a real model.
- Fixtures must be maintained as domain behavior evolves.

## Consequences

Model-based and human evaluation may be added later, but cannot replace deterministic contract tests for budgets, permissions, schemas and citation validity.
