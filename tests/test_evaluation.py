from __future__ import annotations

import unittest

from agent_atelier.evaluation import SCENARIOS, pass_rate, run_evaluation


class EvaluationTests(unittest.TestCase):
    def test_all_declared_scenarios_pass(self) -> None:
        results = run_evaluation()

        self.assertEqual(len(results), len(SCENARIOS))
        self.assertTrue(all(result.passed for result in results))
        self.assertEqual(pass_rate(results), 1.0)

    def test_scenario_ids_are_unique(self) -> None:
        scenario_ids = [scenario.scenario_id for scenario in SCENARIOS]

        self.assertEqual(len(scenario_ids), len(set(scenario_ids)))

    def test_evaluation_results_are_explainable(self) -> None:
        for result in run_evaluation():
            self.assertTrue(result.checks)
            self.assertTrue(result.description)
            self.assertTrue(result.expected_status)
            self.assertTrue(result.actual_status)


if __name__ == "__main__":
    unittest.main()
