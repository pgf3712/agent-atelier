# Chapter 8 — Human approval

## Objective

Pause sensitive side effects and grant narrowly scoped permission that cannot be reused.

## Interactive lab

Propose exporting brief `B-001` as Markdown. Approve or deny it. Approval produces a capability tied to the exact action and arguments; using it consumes it. A second use fails.

The demo does not actually write a file. It teaches the authorization transition separately from the side effect.

## Exercise

Approve Markdown export, then attempt PDF export using the same capability. Explain why the argument digest must reject it.

## Common mistakes

- Asking for approval after performing the action.
- Treating a global “yes” as permission for later actions.
- Reusing approval tokens.
- Showing an approval dialog without arguments or consequences.

## Interview question

**Which actions require human approval?**

Actions with meaningful external effects, irreversible changes, sensitive disclosure or spending should pause. Agent Atelier binds approval to one action and exact arguments, then consumes it once.
