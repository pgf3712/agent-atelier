"""Deterministic abstract cost and latency accounting."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CostPolicy:
    max_cost_units: int
    max_latency_ms: int
    input_unit_size: int = 100
    output_unit_size: int = 50

    def __post_init__(self) -> None:
        if min(self.max_cost_units, self.max_latency_ms, self.input_unit_size, self.output_unit_size) < 1:
            raise ValueError("Cost policy values must be positive integers.")


@dataclass(frozen=True)
class UsageEstimate:
    input_units: int
    output_units: int
    tool_units: int
    total_cost_units: int
    latency_ms: int
    within_cost_budget: bool
    within_latency_budget: bool


def estimate_usage(
    *, input_characters: int, output_characters: int, tool_calls: int, latency_ms: int, policy: CostPolicy
) -> UsageEstimate:
    if min(input_characters, output_characters, tool_calls, latency_ms) < 0:
        raise ValueError("Usage values must not be negative.")
    input_units = _ceiling_division(input_characters, policy.input_unit_size)
    output_units = _ceiling_division(output_characters, policy.output_unit_size)
    tool_units = tool_calls * 2
    total = input_units + output_units + tool_units
    return UsageEstimate(
        input_units=input_units,
        output_units=output_units,
        tool_units=tool_units,
        total_cost_units=total,
        latency_ms=latency_ms,
        within_cost_budget=total <= policy.max_cost_units,
        within_latency_budget=latency_ms <= policy.max_latency_ms,
    )


def _ceiling_division(value: int, size: int) -> int:
    return (value + size - 1) // size
