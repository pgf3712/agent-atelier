from __future__ import annotations

import unittest
import re
from pathlib import Path

from agent_atelier.i18n import load_catalog, translate, validate_catalogs


class TranslationTests(unittest.TestCase):
    def test_catalogs_have_identical_keys(self) -> None:
        validate_catalogs()

    def test_unknown_locale_falls_back_to_english(self) -> None:
        self.assertEqual(load_catalog("fr")["nav.home"], "Home")

    def test_template_values_are_interpolated(self) -> None:
        self.assertEqual(translate("run.progress", "es", current=2, total=6), "Paso 2 de 6")

    def test_english_is_canonical_default(self) -> None:
        self.assertEqual(translate("language.label"), "Language")

    def test_every_html_translation_reference_exists(self) -> None:
        root = Path(__file__).resolve().parents[1]
        html = (root / "web" / "index.html").read_text(encoding="utf-8")
        referenced = set(
            re.findall(r'data-i18n(?:-placeholder|-aria)?="([^"]+)"', html)
        )
        available = set(load_catalog("en"))

        self.assertEqual(referenced - available, set())

    def test_html_has_basic_accessibility_landmarks(self) -> None:
        root = Path(__file__).resolve().parents[1]
        html = (root / "web" / "index.html").read_text(encoding="utf-8")

        self.assertIn('<html lang="en">', html)
        self.assertIn('<main id="workspace">', html)
        self.assertIn('class="skip-link"', html)
        self.assertIn('aria-live="polite"', html)


if __name__ == "__main__":
    unittest.main()
