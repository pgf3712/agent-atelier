# Security Policy

## Current scope

Agent Atelier is an educational local application. The default simulated provider uses no network or API key. It is not presented as production-ready.

## Security boundaries

- Model/provider output is treated as an untrusted action proposal.
- Only explicitly registered tools may execute.
- Tool arguments are validated before execution.
- Budgets and terminal states are enforced by application code.
- A cooperative wall-clock budget stops between provider and tool actions; real network adapters must additionally enforce transport-level timeouts.
- Final citations must refer to evidence returned during the run.
- The educational default exposes no shell, arbitrary file read or unrestricted network tool.
- Public events must not expose secrets or private reasoning.
- The optional real-provider path accepts secrets only from the local process environment. The web interface has no API-key field and the request schema does not accept browser-supplied credentials.

## Reporting a vulnerability

Use GitHub's private vulnerability-reporting option when it is enabled for the repository. Do not open a public issue containing secrets, personal data or an exploitable proof involving real systems. For ordinary non-sensitive bugs, use the repository's bug-report template.

## Supported versions

The latest `0.1.x` release receives security fixes. This remains an educational project, not a supported production service.

## Known limitations

- The preview server is intended only for `127.0.0.1` local development.
- The preview refuses non-loopback binding unless the operator explicitly passes `--allow-remote`; doing so does not add authentication or make the service production-safe.
- Static and JSON responses include a restrictive content security policy, anti-framing, MIME-sniffing and referrer protections.
- Authentication and multi-user isolation are not implemented.
- The educational real-provider adapter is not a production credential gateway. The Windows launcher prompts outside the browser and limits the key to the preview process lifetime; hosted deployments still need managed server-side secrets.
- The quality workflow runs deterministic tests, compilation, JavaScript syntax validation, evaluation and a public-file privacy audit. Repository-level secret scanning should also be enabled in GitHub settings.
