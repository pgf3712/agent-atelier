# Chapter 1 — The smallest bounded loop

## Objective

Read and explain the minimal loop that turns action proposals into a safe, finite run.

## The loop

The implementation lives in `src/agent_atelier/engine.py`:

1. Validate the research question.
2. Create explicit run state.
3. Ask the provider for a structured action.
4. Validate the action kind and required fields.
5. Detect repeated calls.
6. Check step and tool-call budgets.
7. Execute only an allowlisted tool.
8. Add returned evidence to state.
9. Accept a final answer only when all citations exist in state.
10. Stop with a named status.

## Why bounded?

Without enforced stop conditions, a model can repeat a tool, consume unbounded time or continue after it has no useful evidence. The prompt may ask it to stop, but the application must guarantee the boundary.

Current enforced endings are:

- `completed`
- `insufficient_evidence`
- `budget_exhausted`
- `blocked`
- `failed` (reserved for a later error policy)

## Try it

Run:

```bash
PYTHONPATH=src python -m agent_atelier.cli "How do agent budgets improve safety?"
```

Then set the tool budget to zero in the web preview. The provider still proposes a search, but the engine prevents execution.

## Exercise

Add a provider fixture that proposes an answer with citation `E-999`. Predict the terminal status before running the test.

Expected result: `blocked`, because evidence IDs are capabilities created by tool results; the provider cannot invent one.

## Common mistakes

- Counting only successful tool calls instead of attempted executions.
- Keeping the step limit only in the prompt.
- Treating a provider’s JSON as trusted because it parsed successfully.
- Returning a polished answer after evidence search returned no matches.

## Knowledge check

**How do you prevent infinite loops?**

Agent Atelier enforces maximum steps and tool calls in application code, records action fingerprints to detect repetition, and uses explicit terminal states. These controls do not depend on the provider following instructions.
