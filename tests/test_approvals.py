from __future__ import annotations

import unittest

from agent_atelier.approvals import ApprovalStatus, ApprovalStore


class ApprovalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = ApprovalStore()
        self.arguments = {"format": "markdown", "brief_id": "B-001"}

    def test_approved_request_can_be_consumed_once(self) -> None:
        request = self.store.propose("export_brief", self.arguments, "Save the reviewed brief")
        approved = self.store.resolve(request.request_id, approve=True)
        token = approved.token
        consumed = self.store.consume(request.request_id, token or "", "export_brief", self.arguments)
        self.assertEqual(consumed.status, ApprovalStatus.CONSUMED)
        with self.assertRaises(ValueError):
            self.store.consume(request.request_id, token or "", "export_brief", self.arguments)

    def test_denied_request_cannot_execute(self) -> None:
        request = self.store.propose("export_brief", self.arguments, "Save")
        self.store.resolve(request.request_id, approve=False)
        with self.assertRaises(ValueError):
            self.store.consume(request.request_id, "none", "export_brief", self.arguments)

    def test_approval_is_scoped_to_exact_arguments(self) -> None:
        request = self.store.propose("export_brief", self.arguments, "Save")
        approved = self.store.resolve(request.request_id, approve=True)
        with self.assertRaises(ValueError):
            self.store.consume(request.request_id, approved.token or "", "export_brief", {"format": "pdf"})

    def test_unknown_action_cannot_request_approval(self) -> None:
        with self.assertRaises(ValueError):
            self.store.propose("delete_computer", {}, "Please")


if __name__ == "__main__":
    unittest.main()
