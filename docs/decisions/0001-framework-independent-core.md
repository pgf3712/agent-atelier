# ADR 0001: Build a framework-independent core

## Context

The project must teach agent mechanics directly, keep the learning path readable and avoid hiding essential decisions behind a large orchestration framework.

## Decision

The domain loop, actions, budgets, tool registry, evidence model and events are implemented inside this project and depend on no agent framework. Providers are replaceable ports. The deterministic provider is the default.

## Alternatives

- Build the tutorial directly on LangGraph or another orchestration framework.
- Use a real hosted model from the first chapter.
- Present only a high-level workflow without an inspectable loop.

## Advantages

- Mechanisms remain readable and easy to inspect.
- Tests are deterministic, free and offline.
- Provider or framework changes do not redefine the domain.

## Disadvantages

- More orchestration code must be designed and maintained.
- The educational core is intentionally less feature-rich than established frameworks.

## Consequences

Framework integrations, if added, live in adapters and are never required for the main learning path.
