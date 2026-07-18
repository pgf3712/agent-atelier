# Chapter 0 — Agent, workflow or chatbot?

## Objective

Recognize what makes a system agentic without treating every LLM application as an agent.

## Mental model

- **Chatbot:** receives a message and produces a reply. It may have instructions, but it does not necessarily act.
- **Workflow:** follows a sequence chosen by the developer. Branches are explicit and predictable.
- **Agent:** receives a goal and may choose among allowed actions while the application enforces limits and permissions.

An agent is not simply “an LLM that can call functions.” The surrounding application must validate proposed actions, execute tools, return observations and decide when the run must stop.

```text
goal → provider proposes action → application validates → tool executes
  ↑                                                   ↓
  └──────────── state + safe observation ─────────────┘
```

## In Agent Atelier

`SimulatedProvider` proposes an `AgentAction`. It never executes a tool. `run_agent` owns the loop, checks the budget, rejects unknown tools, executes allowed tools and validates the final citations.

That boundary is deliberate: model output is a proposal, not authority.

## Exercise

Classify each system and explain why:

1. A fixed script retrieves sales data and emails the same report every Monday.
2. A support assistant chooses between searching documentation, requesting an order ID and escalating to a person.
3. A chat interface rewrites a paragraph without tools.

Suggested classification: workflow, agent, chatbot. A strong answer discusses who chooses the next action and which boundaries remain under application control.

## Common mistake

Calling a deterministic workflow an agent because it uses an LLM. The model used inside a step does not determine the architecture of the whole system.

## Interview question

**Why did you build the provider and engine separately?**

Because a provider can be unreliable or replaced. The engine must keep authority over tool execution, budgets, validation and observable state regardless of which model proposes an action.
