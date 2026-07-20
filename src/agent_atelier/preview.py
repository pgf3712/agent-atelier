"""Zero-dependency local preview server for Agent Atelier."""

from __future__ import annotations

import argparse
import json
import threading
import webbrowser
from dataclasses import asdict
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from agent_atelier.approvals import ApprovalStore
from agent_atelier.costs import CostPolicy, estimate_usage
from agent_atelier.domain import Budget
from agent_atelier.engine import run_agent
from agent_atelier.evaluation import pass_rate, run_evaluation
from agent_atelier.guardrails import assess_untrusted_content, wrap_untrusted_data
from agent_atelier.final_app import run_research_brief
from agent_atelier.memory import SessionMemory, build_context_snapshot
from agent_atelier.observability import public_event
from agent_atelier.planning import create_research_plan
from agent_atelier.real_provider import build_provider, provider_status
from agent_atelier.tools import ToolError, execute_tool, public_tool_catalog

ROOT = Path(__file__).resolve().parents[2]
TEACHING_MEMORY = SessionMemory()
TEACHING_PLANS: dict[str, object] = {}
TEACHING_APPROVALS = ApprovalStore()


def _validate_bind_target(host: str, allow_remote: bool) -> None:
    normalized = host.strip().lower()
    if not normalized:
        raise ValueError("Host must not be empty.")
    if normalized not in {"127.0.0.1", "localhost", "::1"} and not allow_remote:
        raise ValueError(
            "Refusing to expose the educational preview beyond this computer. "
            "Pass --allow-remote only after reviewing the security limitations."
        )


def _run_payload(payload: dict[str, Any]) -> dict[str, Any]:
    question = payload.get("question")
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    max_steps = payload.get("max_steps", 6)
    max_tool_calls = payload.get("max_tool_calls", 3)
    max_duration_ms = payload.get("max_duration_ms", 5_000)
    if not all(isinstance(value, int) for value in (max_steps, max_tool_calls, max_duration_ms)):
        raise ValueError("Budget values must be integers.")

    provider_name = payload.get("provider", "simulated")
    if not isinstance(provider_name, str):
        raise ValueError("Provider must be a string.")
    state = run_agent(
        question,
        build_provider(provider_name),
        Budget(
            max_steps=max_steps,
            max_tool_calls=max_tool_calls,
            max_duration_ms=max_duration_ms,
        ),
    )
    return {
        "status": state.status.value,
        "steps": state.steps,
        "tool_calls": state.tool_calls,
        "duration_ms": state.duration_ms,
        "answer": state.answer,
        "citations": list(state.citations),
        "evidence": [asdict(item) for item in state.evidence],
        "events": [asdict(event) for event in state.events],
    }


class PreviewHandler(SimpleHTTPRequestHandler):
    """Serve repository files and a single local-only agent endpoint."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; style-src 'self'; "
            "script-src 'self'; connect-src 'self'; object-src 'none'; "
            "base-uri 'none'; frame-ancestors 'none'",
        )
        super().end_headers()

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/":
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", "/web/")
            self.end_headers()
            return
        if self.path == "/api/health":
            self._send_json(HTTPStatus.OK, {"status": "ok", "provider": "simulated"})
            return
        if self.path == "/api/tools":
            self._send_json(HTTPStatus.OK, {"tools": public_tool_catalog()})
            return
        if self.path == "/api/provider-status":
            self._send_json(HTTPStatus.OK, provider_status())
            return
        if self.path == "/api/evaluation":
            evaluation = run_evaluation()
            self._send_json(
                HTTPStatus.OK,
                {"pass_rate": pass_rate(evaluation), "results": [asdict(item) for item in evaluation]},
            )
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in {"/api/run", "/api/tool-demo", "/api/memory-demo", "/api/plan-demo", "/api/event-demo", "/api/guardrail-demo", "/api/approval-demo", "/api/cost-demo", "/api/final-demo"}:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 20_000:
                raise ValueError("Request body size is invalid.")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("JSON body must be an object.")
            if self.path == "/api/final-demo":
                if "api_key" in payload:
                    raise ValueError(
                        "Credentials are not accepted from the browser. "
                        "Use the environment-only local launcher."
                    )
                question = payload.get("question")
                locale = payload.get("locale", "en")
                provider_name = payload.get("provider", "simulated")
                max_steps, max_tool_calls, max_cost_units = payload.get("max_steps", 6), payload.get("max_tool_calls", 3), payload.get("max_cost_units", 30)
                if not isinstance(question, str) or locale not in {"en", "es"} or not isinstance(provider_name, str) or not all(isinstance(value, int) for value in (max_steps, max_tool_calls, max_cost_units)):
                    raise ValueError("Final demo requires a question and integer budgets.")
                result = run_research_brief(question, max_steps=max_steps, max_tool_calls=max_tool_calls, max_cost_units=max_cost_units, locale=locale, provider=build_provider(provider_name))
            elif self.path == "/api/approval-demo":
                action = payload.get("action")
                arguments = {"format": "markdown", "brief_id": "B-001"}
                if action == "propose":
                    approval = TEACHING_APPROVALS.propose("export_brief", arguments, "Export the reviewed brief")
                elif action in {"approve", "deny"}:
                    request_id = payload.get("request_id")
                    if not isinstance(request_id, str):
                        raise ValueError("request_id must be a string.")
                    approval = TEACHING_APPROVALS.resolve(request_id, approve=action == "approve")
                elif action == "consume":
                    request_id, token = payload.get("request_id"), payload.get("token")
                    if not isinstance(request_id, str) or not isinstance(token, str):
                        raise ValueError("request_id and token must be strings.")
                    approval = TEACHING_APPROVALS.consume(request_id, token, "export_brief", arguments)
                else:
                    raise ValueError("Unknown approval-demo action.")
                result = {
                    "request_id": approval.request_id, "action": approval.action,
                    "explanation": approval.explanation, "status": approval.status.value,
                    "token": approval.token,
                }
            elif self.path == "/api/cost-demo":
                values = {name: payload.get(name) for name in ("input_characters", "output_characters", "tool_calls", "latency_ms", "max_cost_units", "max_latency_ms")}
                if not all(isinstance(value, int) for value in values.values()):
                    raise ValueError("All cost-demo values must be integers.")
                usage = estimate_usage(
                    input_characters=values["input_characters"], output_characters=values["output_characters"],
                    tool_calls=values["tool_calls"], latency_ms=values["latency_ms"],
                    policy=CostPolicy(values["max_cost_units"], values["max_latency_ms"]),
                )
                result = asdict(usage)
            elif self.path == "/api/guardrail-demo":
                source_id = payload.get("source_id")
                content = payload.get("content")
                if not isinstance(source_id, str) or not isinstance(content, str):
                    raise ValueError("source_id and content must be strings.")
                result = wrap_untrusted_data(assess_untrusted_content(source_id, content))
            elif self.path == "/api/plan-demo":
                action = payload.get("action", "create")
                plan_id = str(payload.get("plan_id", "local-plan"))
                if action == "create":
                    question = payload.get("question")
                    locale = payload.get("locale", "en")
                    if not isinstance(question, str) or locale not in {"en", "es"}:
                        raise ValueError("question must be a string.")
                    TEACHING_PLANS[plan_id] = create_research_plan(question, locale)
                elif action == "advance":
                    if plan_id not in TEACHING_PLANS:
                        raise ValueError("Create a plan before advancing it.")
                    TEACHING_PLANS[plan_id].complete_active()  # type: ignore[attr-defined]
                else:
                    raise ValueError("Unknown plan-demo action.")
                result = TEACHING_PLANS[plan_id].as_dict()  # type: ignore[attr-defined]
            elif self.path == "/api/event-demo":
                event_type = payload.get("event_type")
                event_payload = payload.get("payload")
                if not isinstance(event_type, str) or not isinstance(event_payload, dict):
                    raise ValueError("event_type must be a string and payload must be an object.")
                result = public_event(event_type, event_payload)
            elif self.path == "/api/memory-demo":
                session_id = payload.get("session_id", "local-learner")
                action = payload.get("action")
                if not isinstance(session_id, str) or not isinstance(action, str):
                    raise ValueError("session_id and action must be strings.")
                if action == "remember":
                    fact = payload.get("fact")
                    if not isinstance(fact, str):
                        raise ValueError("fact must be a string.")
                    facts = TEACHING_MEMORY.remember(session_id, fact)
                elif action == "reset_run":
                    facts = TEACHING_MEMORY.recall(session_id)
                elif action == "clear_memory":
                    TEACHING_MEMORY.clear(session_id)
                    facts = ()
                else:
                    raise ValueError("Unknown memory-demo action.")
                run_number = payload.get("run_number", 1)
                if not isinstance(run_number, int) or run_number < 1:
                    raise ValueError("run_number must be a positive integer.")
                result = {
                    "run_state": {"run_number": run_number, "temporary_note": f"Temporary value for run {run_number}"},
                    "context": build_context_snapshot(
                        question=f"Demo question for run {run_number}", run_step=1,
                        evidence_ids=[], remembered_facts=facts,
                    ),
                    "memory": {"session_id": session_id, "facts": list(facts)},
                }
            elif self.path == "/api/tool-demo":
                tool_name = payload.get("tool_name")
                arguments = payload.get("arguments")
                if not isinstance(tool_name, str) or not isinstance(arguments, dict):
                    raise ValueError("tool_name must be a string and arguments must be an object.")
                evidence = execute_tool(tool_name, arguments)
                result = {
                    "status": "accepted",
                    "tool_name": tool_name,
                    "evidence_ids": [item.evidence_id for item in evidence],
                }
            else:
                result = _run_payload(payload)
        except ToolError as exc:
            self._send_json(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {"status": "blocked", "error": str(exc)},
            )
            return
        except (ValueError, json.JSONDecodeError) as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        self._send_json(HTTPStatus.OK, result)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"[preview] {self.address_string()} - {format % args}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview Agent Atelier locally.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument(
        "--allow-remote",
        action="store_true",
        help="Allow binding beyond localhost. Not recommended for the educational preview.",
    )
    args = parser.parse_args()

    try:
        _validate_bind_target(args.host, args.allow_remote)
    except ValueError as exc:
        parser.error(str(exc))
    server = ThreadingHTTPServer((args.host, args.port), PreviewHandler)
    url = f"http://{args.host}:{args.port}/web/"
    print("Agent Atelier is running locally.")
    print(f"Open: {url}")
    print("Press Ctrl+C in this window to stop it.")
    if not args.no_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAgent Atelier stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
