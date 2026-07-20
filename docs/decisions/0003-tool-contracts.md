# ADR 0003: Application-owned tool contracts

## Context

Providers can emit malformed, excessive or malicious tool arguments. JSON parsing alone provides no authorization or semantic validation.

## Decision

Every executable tool is registered by the application with a stable name, description, argument contract and handler. Unknown tools and unexpected arguments are rejected. A separate public catalog exposes metadata without executable callables.

## Alternatives

- Let handlers validate their own arguments independently.
- Dynamically expose all decorated Python functions.
- Trust provider-generated JSON after parsing.
- Adopt Pydantic immediately for the first zero-dependency slice.

## Advantages

- One visible permission boundary.
- Consistent, testable validation errors.
- Safe metadata can drive documentation and UI.
- The offline preview retains zero runtime dependencies.

## Disadvantages

- The initial schema system supports only a deliberately small constraint set.
- Complex nested schemas would duplicate mature validation-library behavior.

## Consequences

The educational chapters first expose the mechanism. A later adapter may translate Pydantic or JSON Schema models into the same domain contract, but authorization remains in the registry rather than in provider metadata.
