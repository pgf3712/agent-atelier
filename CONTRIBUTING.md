# Contributing

Paula & Indy's Agent Atelier is an educational portfolio project. Contributions should preserve its original learning design, offline-first path and safety boundaries.

## Local setup

```bash
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows Command Prompt: `.venv\Scripts\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

Install for development:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Required checks

```bash
python -m unittest discover -s tests -v
python -m agent_atelier.evaluate_cli
python -m ruff check .
python scripts/release_audit.py
```

## Contribution rules

- Do not copy code, prose, exercises, diagrams or assets from third-party repositories.
- Do not add secrets, personal paths or real user data.
- Do not add a tool without a permission classification and tests.
- Do not show hidden chain of thought; add designed public events and concise rationales.
- Keep English and Spanish translation keys aligned.
- Record every external asset and license before committing it.
- Add or update an ADR when changing a significant architectural decision.
- Keep the simulated provider and essential tests usable without network access.

## Pull request evidence

A change should state what changed, why, tests run, screenshots for visual changes, accessibility impact and any third-party rights impact.
