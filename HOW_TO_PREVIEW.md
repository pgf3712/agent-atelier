# How to preview Agent Atelier on Windows

## Easiest option

1. Open the `paula-indy-agent-atelier` folder.
2. Double-click `OPEN_AGENT_ATELIER.bat`.
3. Keep the terminal window open while using the application.
4. Your browser should open at `http://127.0.0.1:8765/web/`.
5. To stop the application, return to the terminal and press `Ctrl+C`, or close that terminal window.

The preview runs only on your own computer. It uses the deterministic simulated provider, requires no API key and does not access the internet.

It refuses non-local network binding by default. Do not use `--allow-remote` unless you understand that this educational single-user server has no authentication.

## If the browser does not open automatically

Keep the terminal window open and manually visit:

`http://127.0.0.1:8765/web/`

## What you can test now

- Switch between English and Spanish.
- Open chapters 0–10 from the Learning Path; each has a distinct interactive lab.
- Mark a chapter as completed and continue with Next chapter.
- Close and reopen the browser to verify that chapter progress persists.
- Switch between Learning Mode and Workshop Mode.
- Change the maximum step and tool-call budgets.
- Run a question about agent safety, evidence, tools or budgets.
- Try an unrelated question, such as the weather on Neptune, and observe the honest insufficient-evidence result.
- Inspect the public event timeline, evidence cards and metrics.

Paula and Indy use independent transparent chapter portraits. Click Paula for a technical deep dive and Indy for optional progressive help.
