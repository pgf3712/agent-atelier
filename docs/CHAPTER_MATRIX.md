# Chapter implementation matrix

This matrix is the audit trail connecting each learning objective to repository files, a construction checkpoint, a distinct interface lab, executable implementation and bilingual lesson.

| Chapter | Files assembled in the workshop | Typed construction checkpoint | Behaviour proved in the lab |
|---|---|---|---|
| 0 | Packaging, domain actions, provider protocol | Identify `ActionProvider` as the model/application boundary | Classify who controls execution |
| 1 | Budget state, bounded engine, engine tests | Complete `max_steps` in the loop | Reach both completed and budget-exhausted states |
| 2 | Tool contract and tool tests | Place `validate_arguments` before the handler | Accept valid arguments and block malformed ones |
| 3 | Session memory and isolation tests | Scope facts with `session_id` | Reset run state while preserving only session memory |
| 4 | Structured plan and plan tests | Add a `success_condition` | Advance steps only when application-owned proof exists |
| 5 | Public events and observability tests | Apply `redact` to event payloads | Publish safe facts, redact secrets and reject private reasoning |
| 6 | Guardrail wrapper and attack tests | Mark data `UNTRUSTED_DATA_DO_NOT_EXECUTE` | Detect injected instructions without executing them |
| 7 | Evaluation scenarios, runner and tests | State the `expected_status` | Pass five deterministic behavioural cases |
| 8 | Approval capability and replay tests | `consume` a permission before execution | Use one exact approval once |
| 9 | Usage policy and independent-budget tests | Enforce `max_cost_units` | Distinguish cost failure from latency failure |
| 10 | Final composition, preview boundary and integration tests | Select `SimulatedProvider` as the offline default | Produce grounded/insufficient outcomes and optionally swap provider |

Every workshop exposes three construction steps in dependency order, sometimes revisiting the same file to add a second responsibility. Running a displayed command produces an explicitly labelled simulation of the expected terminal result; it never pretends to edit the learner's disk. The typed checkpoint requires the learner to complete a meaningful identifier. Only after both the construction checkpoint (`built`) and the chapter-specific lab evidence exist can the completion button unlock.
