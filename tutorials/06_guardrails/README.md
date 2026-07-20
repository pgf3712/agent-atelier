# Chapter 6 — Guardrails and untrusted data

## Objective

Keep provider output and retrieved documents inside explicit data boundaries.

## Interactive lab

Inspect a normal source and a source containing “ignore previous instructions.” Both remain classified as untrusted retrieved data; the suspicious one adds a warning. Neither can grant execution permission.

Pattern detection is defense in depth, not a complete injection solution. The stronger control is architectural: retrieved text is data, tools remain allowlisted, and application policy owns execution.

## Exercise

Add an oversized document and verify it is rejected before storage or provider use. Then add a benign sentence containing the word “instructions” and avoid a false positive.

## Common mistakes

- Asking the same model to decide whether content is safe and then blindly trusting it.
- Treating “trusted website” as trusted instructions.
- Solving injection only with a prompt sentence.
- Giving retrieved content access to unrestricted tools.

## Knowledge check

**How do you mitigate prompt injection?**

Agent Atelier marks retrieved text as untrusted data, applies size and warning checks, never lets content alter the tool allowlist, validates every proposed action and keeps sensitive operations behind application policy.
