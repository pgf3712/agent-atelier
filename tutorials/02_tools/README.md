# Chapter 2 — Typed tools and schemas

## Objective

Understand why a tool call is an untrusted proposal and how the application turns it into a validated operation.

## Mental model

A tool has four separate parts:

1. A stable name the provider may propose.
2. A user-facing description of its purpose.
3. An argument contract owned by the application.
4. A handler that the application—not the provider—may execute.

```text
provider JSON
     ↓ untrusted
tool name allowlist
     ↓
required fields → types → constraints → reject extras
     ↓ validated
application invokes handler
```

## The Agent Atelier contract

`ArgumentSpec` currently records:

- Python value type.
- Human-readable description.
- Whether the field is required.
- Minimum string length.

`validate_arguments` rejects:

- A non-object argument payload.
- Missing required fields.
- Incorrect types.
- Empty normalized search queries.
- Unexpected fields.

Rejecting unexpected fields matters. A provider must not smuggle an unreviewed `path`, `url` or `command` into a tool whose contract only permits `query`.

## Tool discovery

`public_tool_catalog()` exposes only safe metadata. It does not expose Python callables. The local preview serves that catalog through `GET /api/tools`, allowing the future Tools screen and tutorial to use the same source of truth as the engine.

## Exercise

Extend `ArgumentSpec` with an optional maximum string length and add tests for a query that exceeds it. Decide whether normalization happens before or after the length check and explain the trade-off.

Expected design: normalize first so surrounding whitespace does not consume the limit, then reject the normalized oversized input before the handler runs.

## Common mistakes

- Assuming valid JSON is valid tool input.
- Letting the provider choose an arbitrary function name.
- Ignoring unexpected arguments.
- Putting validation inside every handler and producing inconsistent errors.
- Showing raw internal exceptions to users.
- Treating a tool description as a security control.

## Interview question

**How do you validate tool calls?**

Agent Atelier resolves the proposed name through an explicit registry, validates the complete argument object against an application-owned contract, rejects missing, mistyped or unexpected fields, and only then calls the handler. The provider never receives a direct Python callable or execution authority.
