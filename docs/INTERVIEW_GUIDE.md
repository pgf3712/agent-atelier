# How to discuss Agent Atelier in an interview

## What is the project?

Agent Atelier is a bilingual, offline-first learning laboratory that exposes the internal mechanics of an AI agent. Its deterministic provider lets every chapter, test and GitHub check run without an API key or model cost.

## Is it an agent or a workflow?

The engine is an agent loop because the provider selects the next structured action from the current run state. It is still bounded by workflow-like policy: the application owns the allowlist, schemas, budgets and terminal states. The final result is intentionally more constrained than an autonomous general-purpose agent.

## Why implement the loop directly?

The teaching goal is to make authority visible. `engine.py` shows where an action is proposed, validated, executed and recorded. A framework integration could be added later, but hiding this sequence would weaken the lesson and make interview explanations dependent on library abstractions.

## How are infinite loops prevented?

The engine enforces maximum steps, tool calls and cooperative elapsed time. It also fingerprints tool actions and blocks exact repetitions. These controls are independent, so reducing one budget does not silently change the others.

## How are tools kept safe?

Only registered tools can execute. Arguments are checked against explicit contracts; missing, extra or incorrectly typed fields are rejected before the implementation runs. The teaching tool searches only a bundled in-memory corpus and cannot read arbitrary paths or invoke the shell.

## What does the provider control?

Only the proposed next action. It cannot execute a tool, expand its budget, approve a sensitive operation or validate its own citations. Those decisions remain in application code.

## How are state and memory different?

Run state is temporary execution data. Context is the selected information passed into a decision. Session memory is information deliberately retained across runs. Chapter 3 displays the three separately so persistence is never accidental.

## How is observability handled without exposing private reasoning?

The engine emits versioned public events describing actions, validated tool calls, outcomes and policy decisions. Secret-like fields are redacted and private-reasoning event types are rejected. The UI presents these events, not hidden chain of thought.

## How is prompt injection handled?

Retrieved text is classified and wrapped as untrusted data. Known instruction-like patterns produce warnings, but the central protection is architectural: retrieved content is never given authority to change the system policy or tool permissions. Pattern detection alone is not presented as a complete defence.

## How is human approval scoped?

Approval is bound to one action and its exact arguments. The capability token is single-use and consumed after execution. Reusing it or changing the arguments fails.

## How is the agent evaluated?

Five deterministic behavioural scenarios check grounded completion, insufficient evidence, zero tool budget, forbidden tools and invented citations. Each scenario has explicit expected status and checks; the report is reproducible in CI.

## Are the cost figures real?

No. Chapter 9 uses clearly labelled abstract units derived from characters and tool calls. This demonstrates independent cost and latency policy without pretending local character counts are provider tokens or currency.

## What would change for production?

A production version needs a threat-modelled provider adapter, transport timeouts, authentication, rate limits, durable storage, multi-user isolation, secret management, structured telemetry, dependency/secret scanning and deployment-specific evaluation. The built-in HTTP server is deliberately a local preview, not a production server.

## Strong closing summary

> I built the core loop myself so the repository can teach where authority, validation and stopping conditions actually live. Then I made those decisions observable, testable and bilingual, with a deterministic provider so anyone can reproduce the behaviour without paying for an API.
