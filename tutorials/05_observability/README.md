# Chapter 5 — Events, traces and debugging

## Objective

Observe execution without exposing secrets or private chain of thought.

## Interactive lab

Publish a safe tool event, pass an event containing an API key and attempt to publish a private-reasoning event. The application redacts the secret and rejects the private event type.

Public events explain what happened: proposed action category, validated tool, result identifiers, policy decisions and terminal status. They do not expose hidden scratchpads.

## Exercise

Add a canary secret to a nested list and prove it never appears in serialized public output.

## Common mistakes

- Logging full provider requests and headers.
- Calling private reasoning “observability.”
- Using unversioned event payloads.
- Recording raw tool results without size or sensitivity controls.

## Interview question

**How do you make an agent observable safely?**

Agent Atelier emits versioned, allowlisted event types with redacted payloads. It shows actions and outcomes designed for debugging while explicitly rejecting private-reasoning events.
