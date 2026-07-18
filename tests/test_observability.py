from __future__ import annotations

import unittest

from agent_atelier.observability import public_event, redact


class ObservabilityTests(unittest.TestCase):
    def test_nested_secrets_are_redacted(self) -> None:
        result = redact({"api_key": "abc", "nested": {"token": "xyz", "safe": "ok"}})
        self.assertEqual(result["api_key"], "[REDACTED]")
        self.assertEqual(result["nested"]["token"], "[REDACTED]")
        self.assertEqual(result["nested"]["safe"], "ok")

    def test_secret_patterns_inside_text_are_redacted(self) -> None:
        result = redact("Authorization: Bearer super-secret")
        self.assertNotIn("super-secret", result)
        self.assertIn("[REDACTED]", result)

    def test_public_event_has_schema_version(self) -> None:
        event = public_event("tool.started", {"tool": "search_local_corpus"})
        self.assertEqual(event["schema_version"], "1.0")

    def test_non_public_event_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            public_event("provider.private_reasoning", {"text": "hidden"})


if __name__ == "__main__":
    unittest.main()
