# Optional real model provider

Agent Atelier is fully teachable with `SimulatedProvider`: it is free, deterministic and used by tests. The OpenAI adapter is an optional comparison layer for Chapter 10, not a requirement and not a replacement for the harness.

## What changes

The engine, budgets, tool validation and citation checks remain application-owned. `OpenAIResponsesProvider` replaces only the component that proposes the next action. It uses the Responses API function-calling flow: the model proposes `search_local_corpus`, the application validates and executes it, and the function result is returned to the model. This follows OpenAI's current [function-calling guide](https://developers.openai.com/api/docs/guides/function-calling).

## Install the optional dependency

```powershell
python -m pip install -e ".[real]"
```

## Configure the local server

Create an API key in the OpenAI dashboard and expose it as an environment variable. The official [developer quickstart](https://developers.openai.com/api/docs/quickstart) states that OpenAI SDKs read `OPENAI_API_KEY` from the environment.

Choose a model available to your own API project. Agent Atelier deliberately has no hard-coded model default because availability and model recommendations change.

For the current PowerShell window only:

```powershell
$env:OPENAI_API_KEY="your-key"
$env:AGENT_ATELIER_MODEL="your-enabled-model-id"
$env:AGENT_ATELIER_PROVIDER="openai"
python -m agent_atelier.preview
```

Then open Chapter 10, select the OpenAI provider and acknowledge the external API/cost notice. To return to the free path, select `Simulated` or remove `AGENT_ATELIER_PROVIDER`.

## Safer Windows launcher

After installing the optional dependency, double-click `OPEN_AGENT_ATELIER_REAL.bat`. It asks for the enabled model ID and then requests the API key in a hidden PowerShell prompt. The key never enters the browser, is exposed only to the local preview process and is removed from that process environment when the server closes.

The ordinary `OPEN_AGENT_ATELIER.bat` always starts the free simulator and never asks for a secret. OpenAI's API-key safety guidance recommends environment variables and warns against deploying secrets in client-side applications.

## Security and cost boundaries

- The key stays in the server process environment. It is never accepted through the browser, stored in browser storage, returned in API responses or written by application logs.
- The simulator remains the default. The interface explains when the optional SDK must be installed and requires a model ID plus explicit cost consent for a real request.
- Selecting the real provider requires explicit acknowledgement because the question leaves the computer and API usage may cost money.
- The only exposed function is the repository's allowlisted local corpus search.
- Tool arguments still pass through `validate_arguments` before execution.
- Returned citations still pass through the engine's evidence-ID check.
- The preview remains bound to loopback by default.
- Never commit `.env`, terminal history containing keys or real response logs containing sensitive prompts.

## What this adapter does not claim

It is an educational integration, not a production gateway. A production version needs authentication, per-user quotas, retry/backoff policy, request cancellation, provider-specific usage accounting, audit retention rules and a broader adversarial evaluation set.
