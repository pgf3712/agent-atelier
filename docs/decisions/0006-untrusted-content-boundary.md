# ADR 0006: Retrieved content is always untrusted data

## Context

Documents may contain instructions intended to override the agent or exfiltrate information.

## Decision

All retrieved content receives an untrusted-data classification and explicit non-executable boundary. Size limits and injection-pattern warnings add defense in depth, while tool permissions remain application-owned.

## Alternatives

- Trust content from approved domains.
- Rely only on a system-prompt warning.
- Ask a model to classify content and treat its answer as authorization.

## Consequences

Content can inform an answer but cannot grant permissions. Pattern checks remain intentionally documented as incomplete.
