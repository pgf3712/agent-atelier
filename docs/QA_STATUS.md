# Quality status

Last updated: 2026-07-18

## Automated verification

- All 83 standard-library tests pass on Python 3.14.
- All five deterministic evaluation scenarios pass (100%).
- JavaScript syntax and both English/Spanish JSON catalogues validate.
- GitHub Actions reproduces tests, Python compilation, JavaScript validation and evaluation without secrets or paid APIs.
- English and Spanish catalogues contain identical keys and stable evidence identifiers.
- The preview binds to loopback by default and rejects remote binding without explicit opt-in.
- The optional real-provider adapter is isolated behind the provider protocol and is tested with a deterministic fake client.

## Learning design verified

- Chapters 0–10 have distinct learning objectives, labs, observable evidence and bilingual lessons.
- Every chapter follows **Understand → Build → Test → Explain → Complete**.
- Prediction, code completion and reflection use chapter-specific guided choices instead of arbitrary typing.
- Distractors model realistic misconceptions; feedback now explains the selected model, the safer rule and the evidence to compare.
- Completion remains locked until the relevant construction and behavioural evidence exists.
- Study Mode introduces every concept, example, pitfall, proof and repository file before practice.
- Learning Mode and Workshop Mode expose materially different levels of guidance and information density.
- Paula exposes one next action at a time. Clicking her opens a chapter-specific technical notebook with the mental model, concrete example, common pitfall, file connections and an evidence-based technical summary.
- Indy provides progressive help: contextual hint first, exact answer only after a second deliberate action.
- The curriculum quality matrix records the misconception, safer model and observable proof for all eleven chapters.

## Technical and safety behaviour verified

- The agent loop enforces explicit step, tool, time, cost and latency limits.
- Tool arguments are validated before execution and unknown capabilities are blocked.
- Memory is isolated by session.
- Plans advance only after observable success conditions.
- Public events redact secrets and reject private reasoning event types.
- Retrieved content remains labelled as untrusted data.
- Human approval is scoped to exact arguments and consumed once.
- Grounded, insufficient-evidence, blocked and budget-exhausted outcomes are all tested.
- The browser never accepts a provider API key; the optional launcher holds it only in the local server process.

## Visual and interaction behaviour verified statically

- The original pixel-art studio is a fixed full-page background under translucent navy surfaces.
- Paula and Indy use eleven chapter-specific transparent PNGs each; chapter portraits do not blink, jump or animate.
- Character assets preload, use cache versions and fall back safely if a file cannot load.
- The sleeping sidebar Indy uses only restrained CSS breathing and `Z` motion, disabled by `prefers-reduced-motion`.
- The final reward uses original animated trophy assets, optional confetti and optional procedural celebration audio.
- All translation keys referenced by the HTML exist.
- Basic landmarks, a skip link, keyboard-focus styles and restrained live regions are present.
- The primary palette is midnight navy and slate blue; pink remains a secondary accent.
- Six current-build screenshots were reviewed and added to the bilingual README gallery. They show the learning path, Study Mode, Workshop Mode, Paula's notebook, Indy's help and the completion reward without browser chrome or private information.

## Manual release checks still required

- Open Paula's notebook in both languages and inspect desktop and mobile layout.
- Complete a keyboard-only walkthrough.
- Run an automated contrast audit and a screen-reader smoke test.
