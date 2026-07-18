from __future__ import annotations

import unittest

from agent_atelier.costs import CostPolicy, estimate_usage


class CostTests(unittest.TestCase):
    def test_estimate_uses_ceiling_units_and_tool_weight(self) -> None:
        usage = estimate_usage(input_characters=101, output_characters=51, tool_calls=2, latency_ms=800, policy=CostPolicy(20, 1000))
        self.assertEqual(usage.input_units, 2)
        self.assertEqual(usage.output_units, 2)
        self.assertEqual(usage.tool_units, 4)
        self.assertEqual(usage.total_cost_units, 8)

    def test_cost_and_latency_budgets_are_independent(self) -> None:
        usage = estimate_usage(input_characters=500, output_characters=250, tool_calls=2, latency_ms=1500, policy=CostPolicy(20, 1000))
        self.assertTrue(usage.within_cost_budget)
        self.assertFalse(usage.within_latency_budget)

    def test_negative_usage_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            estimate_usage(input_characters=-1, output_characters=0, tool_calls=0, latency_ms=0, policy=CostPolicy(10, 1000))


if __name__ == "__main__":
    unittest.main()
