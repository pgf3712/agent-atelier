from __future__ import annotations

import unittest

from agent_atelier.planning import StepStatus, create_research_plan


class PlanningTests(unittest.TestCase):
    def test_plan_has_one_active_step_and_success_conditions(self) -> None:
        plan = create_research_plan("How do budgets improve agent safety?")
        self.assertEqual(sum(step.status == StepStatus.ACTIVE for step in plan.steps), 1)
        self.assertTrue(all(step.success_condition for step in plan.steps))

    def test_advancing_completes_active_and_activates_next(self) -> None:
        plan = create_research_plan("Question")
        plan.complete_active()
        self.assertEqual(plan.steps[0].status, StepStatus.COMPLETED)
        self.assertEqual(plan.steps[1].status, StepStatus.ACTIVE)

    def test_plan_eventually_completes(self) -> None:
        plan = create_research_plan("Question")
        for _ in plan.steps:
            plan.complete_active()
        self.assertTrue(plan.completed)

    def test_empty_goal_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_research_plan(" ")

    def test_spanish_plan_translates_teaching_copy_not_domain_identifiers(self) -> None:
        plan = create_research_plan("¿Cómo mejoran la seguridad los presupuestos?", "es")

        self.assertEqual(plan.steps[0].step_id, "P-01")
        self.assertEqual(plan.steps[0].title, "Aclarar la pregunta")
        self.assertEqual(plan.steps[0].status, StepStatus.ACTIVE)


if __name__ == "__main__":
    unittest.main()
