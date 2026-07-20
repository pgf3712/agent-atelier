from __future__ import annotations

import unittest

from agent_atelier.memory import SessionMemory, build_context_snapshot


class MemoryTests(unittest.TestCase):
    def test_memory_persists_across_distinct_run_contexts(self) -> None:
        memory = SessionMemory()
        memory.remember("learner", "Prefer concise explanations")
        first = build_context_snapshot(question="First", run_step=2, evidence_ids=["E-001"], remembered_facts=memory.recall("learner"))
        second = build_context_snapshot(question="Second", run_step=1, evidence_ids=[], remembered_facts=memory.recall("learner"))
        self.assertNotEqual(first["current_question"], second["current_question"])
        self.assertEqual(first["remembered_facts"], second["remembered_facts"])

    def test_sessions_are_isolated(self) -> None:
        memory = SessionMemory()
        memory.remember("paula", "Likes concise examples")
        self.assertEqual(memory.recall("paula"), ("Likes concise examples",))
        self.assertEqual(memory.recall("other"), ())

    def test_duplicate_fact_is_not_added_twice(self) -> None:
        memory = SessionMemory()
        memory.remember("learner", "Use English")
        memory.remember("learner", "Use English")
        self.assertEqual(memory.recall("learner"), ("Use English",))

    def test_invalid_facts_are_rejected(self) -> None:
        memory = SessionMemory()
        with self.assertRaises(ValueError):
            memory.remember("learner", " ")
        with self.assertRaises(ValueError):
            memory.remember("learner", "x" * 201)

    def test_clear_removes_only_selected_session(self) -> None:
        memory = SessionMemory()
        memory.remember("paula", "Keep")
        memory.remember("guest", "Remove")
        memory.clear("guest")
        self.assertEqual(memory.recall("paula"), ("Keep",))
        self.assertEqual(memory.recall("guest"), ())


if __name__ == "__main__":
    unittest.main()
