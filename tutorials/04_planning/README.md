# Chapter 4 — Planning and progress

## Objective

Turn a broad goal into explicit, checkable steps while remembering that a plan is a mutable hypothesis—not a guarantee.

## Interactive lab

Create a research plan, inspect each success condition and use the teaching control to simulate the application receiving proof for the active condition. The next step activates only after that simulated verification.

`ResearchPlan` separates the goal, ordered steps, success conditions and status. The provider does not mark its own work correct; application code advances the plan. In production, the control must be replaced by a check against evidence, a tool result or a human decision.

## Exercise

Add a “revise” operation that returns a completed step to active and records why. Decide whether later completed steps must reopen.

## Common mistakes

- Treating generated plan prose as executable state.
- Creating steps without success conditions.
- Completing several steps because the model says it did them.
- Refusing to revise a plan after new evidence.

## Interview question

**Why model planning explicitly?**

Because structured steps make progress inspectable and testable. Agent Atelier keeps step status under application control and uses success conditions instead of trusting confident plan narration.
