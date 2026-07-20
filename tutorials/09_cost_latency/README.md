# Chapter 9 — Cost, latency and budgets

## Objective

Measure resource usage explicitly and keep cost and latency limits independent.

## Interactive lab

Change input/output size, tool calls and simulated latency. The calculator converts usage into abstract units and reports whether each budget passes. Abstract units avoid pretending a simulated provider has a real vendor price.

## Exercise

Create one configuration that passes cost but fails latency, and another that fails cost but passes latency. Explain why one combined threshold would hide useful information.

## Common mistakes

- Reporting tokens or dollars for a provider that does not return them.
- Checking budget only after the run.
- Treating latency and monetary cost as interchangeable.
- Hiding estimation assumptions.

## Knowledge check

**How do you control agent cost?**

Agent Atelier measures input, output and tool usage, applies an explicit policy and reports estimation assumptions. A real adapter would replace abstract units with provider usage while preserving the same budget boundary.
