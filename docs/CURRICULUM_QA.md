# Curriculum Quality Audit

This audit checks that each activity teaches a distinct mental model instead of rewarding arbitrary clicking.

| Chapter | Misconception tested | Safer mental model | Evidence the learner observes |
|---:|---|---|---|
| 0 | A chatbot is automatically an agent | Agency depends on who selects and executes the next action | Three systems are classified by control ownership |
| 1 | A loop can run until the model feels finished | The application owns hard stopping conditions | Completion and budget exhaustion are both visible states |
| 2 | Tool descriptions are enough validation | Arguments must pass a typed boundary before execution | A valid call runs and a malformed call is blocked |
| 3 | Memory is simply the whole conversation forever | Run state and session memory have different lifetimes | One session persists while another remains isolated |
| 4 | A plausible plan proves progress | Steps advance only after application-owned success evidence | A step stays open until its condition is satisfied |
| 5 | More logs always mean better observability | Public events must be useful, versioned and safe | Secrets are redacted and private reasoning is rejected |
| 6 | Retrieved text can instruct the agent | External content is untrusted data | Injection-like text is labelled and never executed |
| 7 | One successful demo proves quality | Evaluation needs explicit scenarios and expected outcomes | The same five cases run deterministically |
| 8 | Approval is a permanent yes/no flag | Permission should be narrow, explicit and consumable | One exact action is allowed once |
| 9 | Token, cost and latency limits are interchangeable | Independent budgets need independent failures | Cost and latency limits produce different outcomes |
| 10 | A polished answer is necessarily grounded | The final system must connect claims to evidence or admit insufficiency | Grounded and insufficient results are both valid |

## Question design rules

Every prediction or reflection should ask about the chapter's application-owned boundary, include plausible misconceptions, avoid trivia and trick wording, connect the answer to visible evidence, explain why after the answer, and remain solvable without external knowledge.

Indy provides progressive help: a contextual nudge first, then an explicit answer only by deliberate request. Paula provides depth rather than answers: concept, example, pitfall, repository connections and an evidence-based technical summary.

## Scope decision

The beginner path is complete at eleven chapters. Retries and backoff, concurrency and idempotency, multi-agent coordination, authentication, multi-tenancy and production deployment are valuable advanced topics, but adding them to the core path would weaken its focus. They belong in a later **Advanced Atelier** track after the current learning outcomes are validated with users.
