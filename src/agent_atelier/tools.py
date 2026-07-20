"""Explicit, side-effect-free tools used by the first lesson."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable
import unicodedata

from agent_atelier.domain import EvidenceItem


class ToolError(ValueError):
    """A safe error that can be shown in the educational event timeline."""


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    arguments: dict[str, "ArgumentSpec"]
    handler: Callable[[dict[str, Any]], list[EvidenceItem]]


@dataclass(frozen=True)
class ArgumentSpec:
    value_type: type
    description: str
    required: bool = True
    min_length: int | None = None


def validate_arguments(tool: Tool, arguments: dict[str, Any]) -> dict[str, Any]:
    """Validate provider-owned arguments against the application-owned contract."""

    if not isinstance(arguments, dict):
        raise ToolError("Tool arguments must be an object.")

    unexpected = set(arguments) - set(tool.arguments)
    if unexpected:
        names = ", ".join(sorted(unexpected))
        raise ToolError(f"Unexpected argument(s) for '{tool.name}': {names}.")

    validated: dict[str, Any] = {}
    for name, spec in tool.arguments.items():
        if name not in arguments:
            if spec.required:
                raise ToolError(f"Missing required argument '{name}' for '{tool.name}'.")
            continue
        value = arguments[name]
        if not isinstance(value, spec.value_type):
            raise ToolError(
                f"Argument '{name}' for '{tool.name}' must be {spec.value_type.__name__}."
            )
        if isinstance(value, str):
            value = value.strip()
            if spec.min_length is not None and len(value) < spec.min_length:
                raise ToolError(
                    f"Argument '{name}' for '{tool.name}' must contain at least "
                    f"{spec.min_length} character(s)."
                )
        validated[name] = value
    return validated


CORPUS = (
    EvidenceItem(
        "E-001",
        "Bounded agent execution",
        "Step and tool-call limits guarantee that an agent run cannot continue indefinitely.",
        "local://agent-safety/budgets",
    ),
    EvidenceItem(
        "E-002",
        "Structured tool boundaries",
        "Allowlisted tools and validated arguments reduce accidental or unauthorized actions.",
        "local://agent-safety/tools",
    ),
    EvidenceItem(
        "E-003",
        "Evidence-aware answers",
        "An agent should declare insufficient evidence instead of inventing unsupported claims.",
        "local://agent-quality/evidence",
    ),
)

CORPUS_ES = (
    EvidenceItem(
        "E-001",
        "Presupuestos para una ejecución acotada",
        "Los presupuestos y límites de pasos y herramientas garantizan que una ejecución no pueda continuar indefinidamente.",
        "local://agent-safety/budgets",
    ),
    EvidenceItem(
        "E-002",
        "Fronteras estructuradas para herramientas",
        "Una lista permitida y la validación de argumentos reducen acciones accidentales o no autorizadas.",
        "local://agent-safety/tools",
    ),
    EvidenceItem(
        "E-003",
        "Respuestas basadas en evidencias",
        "Un agente debe declarar que la evidencia es insuficiente en lugar de inventar afirmaciones sin respaldo.",
        "local://agent-quality/evidence",
    ),
)

SPANISH_QUERY_MARKERS = {
    "agente", "agentes", "como", "coste", "evidencia", "herramienta",
    "limite", "presupuesto", "seguridad",
}


def _tokens(text: str) -> set[str]:
    """Return comparable, accent-insensitive terms without language libraries."""

    normalized = unicodedata.normalize("NFKD", text.casefold())
    plain = "".join(character for character in normalized if not unicodedata.combining(character))
    return {
        "".join(character for character in word if character.isalnum())
        for word in plain.split()
        if len(word) > 3
    } - {""}


def search_corpus(arguments: dict[str, Any]) -> list[EvidenceItem]:
    query = arguments.get("query")
    if not isinstance(query, str) or not query.strip():
        raise ToolError("'query' must be a non-empty string.")
    words = _tokens(query)
    corpus = CORPUS_ES if words.intersection(SPANISH_QUERY_MARKERS) else CORPUS
    matches = [
        item
        for item in corpus
        if words.intersection(_tokens(f"{item.title} {item.content}"))
    ]
    return matches


TOOLS = {
    "search_local_corpus": Tool(
        name="search_local_corpus",
        description="Search the small, trusted-location corpus for relevant evidence.",
        arguments={
            "query": ArgumentSpec(
                value_type=str,
                description="Research terms to match against the local evidence corpus.",
                min_length=1,
            )
        },
        handler=search_corpus,
    )
}


def execute_tool(name: str, arguments: dict[str, Any]) -> list[EvidenceItem]:
    tool = TOOLS.get(name)
    if tool is None:
        raise ToolError(f"Tool '{name}' is not allowed.")
    return tool.handler(validate_arguments(tool, arguments))


def public_tool_catalog() -> list[dict[str, Any]]:
    """Return a safe, serializable catalog for documentation and the UI."""

    return [
        {
            "name": tool.name,
            "description": tool.description,
            "arguments": {
                name: {
                    "type": spec.value_type.__name__,
                    "description": spec.description,
                    "required": spec.required,
                    "min_length": spec.min_length,
                }
                for name, spec in tool.arguments.items()
            },
        }
        for tool in TOOLS.values()
    ]
