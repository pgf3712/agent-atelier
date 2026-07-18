# Architecture Overview

## Current executable slice

```text
Browser
  │  POST /api/run
  ▼
Local preview adapter
  │  validated question + budget
  ▼
Application engine ─────────────► versioned public events
  │                                  │
  │ asks for an action               └──► bilingual UI timeline
  ▼
Simulated provider
  │ structured action proposal
  ▼
Policy checks: action shape, repetition, budget, allowlist
  │
  ▼
Local corpus tool ───────────────► evidence stored in run state
  │
  ▼
Final-answer citation validation ─► terminal run status
```

## Authority boundary

The provider may propose an action. It cannot execute tools, grant permission, change budgets or declare an unknown citation valid. The application engine owns those decisions.

## Packages

- `domain.py`: statuses, budgets, actions, evidence, events and run state.
- `provider.py`: provider protocol and deterministic implementation.
- `tools.py`: explicit tool registry and local corpus.
- `engine.py`: bounded orchestration and policy enforcement.
- `evaluation.py`: reproducible scenario contracts and metrics.
- `i18n.py`: strict translation catalog loading and parity validation.
- `preview.py`: local-only HTTP adapter for the web demonstration.

## Data flow

1. The browser sends a question and integer budget values.
2. The preview adapter validates request shape and size.
3. The engine creates isolated in-memory run state.
4. The provider proposes a structured action.
5. The engine verifies policy and executes an allowlisted tool.
6. Evidence IDs are added to run state.
7. A final answer is accepted only when every citation exists in that state.
8. The adapter returns public events, evidence and metrics as JSON.

## Present limitations

- State is in memory for one request and is not persisted.
- The local server is intentionally single-user and unauthenticated.
- The simulated provider is not a language model.
- Tool schemas currently use explicit Python validation rather than Pydantic.
- The core enforces a cooperative wall-clock budget between provider/tool actions. It cannot forcibly interrupt a blocking third-party call; a real adapter would also need transport-level timeouts.
- Abstract cost and latency accounting is implemented for the Chapter 9 lab and integrated Chapter 10 view. It deliberately avoids pretending that local character counts are provider tokens or money.
- The UI has not completed cross-browser or accessibility QA.
