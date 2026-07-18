# ADR 0010 — Local preview boundary and cooperative timeout

## Context

The educational interface needs a real Python backend without requiring deployment, authentication or an API key. Agent runs also need a time budget, but the current provider and tools are synchronous and deterministic.

## Decision

The preview binds to a loopback host by default and rejects non-loopback hosts unless the operator passes `--allow-remote`. Responses send restrictive browser security headers. The engine measures elapsed monotonic time and enforces `max_duration_ms` before and after provider/tool actions.

## Alternatives

- Ship only static mock data. Rejected because the interface would not demonstrate the real engine.
- Run a production web framework with authentication. Rejected for the zero-dependency educational slice.
- Forcefully terminate provider calls in threads or subprocesses. Deferred because it would obscure the minimal loop and introduce platform-specific lifecycle complexity.

## Advantages

- Safe local default and explicit network boundary.
- Deterministic timeout tests through an injected clock.
- No API key, network service or runtime dependency.

## Disadvantages

- A cooperative timeout cannot interrupt a provider call that blocks forever.
- `--allow-remote` does not add authentication or multi-user isolation.

## Consequences

Every real provider adapter must add its own connection/read timeout. A production deployment must replace the preview server and threat-model authentication, concurrency, rate limits and storage.
