# Chapter 7 — Reproducible evaluation

## Objective

Replace vague “the agent works” claims with concrete scenarios and exact expected outcomes.

## Interactive lab

Run the same deterministic suite used by the command line and tests. Each case reports expected status, actual status and computable checks.

Current contracts cover a grounded brief, insufficient evidence, zero tool budget, forbidden tool and invented citation.

## Exercise

Create a failing fixture by changing one expected status. Read the report, restore the contract and add a new scenario for malformed arguments.

## Common mistakes

- Measuring only answer style.
- Using one happy-path demo as evaluation.
- Letting a model judge safety controls that have exact deterministic answers.
- Reporting an aggregate score without individual failures.

## Knowledge check

**How do you evaluate an agent?**

Agent Atelier starts with deterministic behavioral contracts for tools, schemas, stopping, budgets and citations. Human or model-based rubrics may later assess language quality, but cannot replace exact safety checks.
