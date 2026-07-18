# Chapter 3 — State, context and memory

## Objective

Separate three concepts that are often incorrectly used as synonyms.

- **Run state** is changing data owned by one execution: step count, evidence and status.
- **Context** is selected information made available for the next decision.
- **Memory** is deliberately retained information that may be recalled in a later run.

Context is a view, not a database. Memory is not every token ever seen. Run state must not silently leak into another session.

## Interactive lab

Save a preference, start another run and compare the three boxes. The temporary run value changes, context is rebuilt, and the remembered fact remains until explicitly cleared. The preview uses an in-memory store, so closing the server clears it intentionally.

## Exercise

Store one fact for session `paula` and another for `guest`. Verify that recall never crosses session identifiers, then clear only `guest`.

## Common mistakes

- Sending the complete database to the model as context.
- Persisting every message as long-term memory.
- Sharing one global memory list across users.
- Letting a provider write memory without application policy.
- Assuming remembered information remains correct forever.

## Interview question

**How do you distinguish state, context and memory?**

State belongs to a current run, context is a bounded selection for a decision, and memory is explicitly retained information that can cross run boundaries. Agent Atelier models and tests those lifetimes separately.
