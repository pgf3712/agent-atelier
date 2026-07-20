import json
import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LearningPathTests(unittest.TestCase):
    def test_all_chapters_have_bilingual_lessons(self) -> None:
        chapter_dirs = sorted((ROOT / "tutorials").glob("[0-9][0-9]_*"))
        self.assertEqual(len(chapter_dirs), 11)
        for chapter in chapter_dirs:
            self.assertTrue((chapter / "README.md").is_file())
            self.assertTrue((chapter / "README.es.md").is_file())

    def test_all_chapters_have_localized_interface_content(self) -> None:
        catalogs = {
            locale: json.loads(
                (ROOT / "src" / "agent_atelier" / "locales" / f"{locale}.json").read_text(
                    encoding="utf-8"
                )
            )
            for locale in ("en", "es")
        }
        for number in range(11):
            for suffix in ("title", "summary", "outcome", "piece", "proof", "pose"):
                key = f"chapter.{number}.{suffix}"
                self.assertTrue(catalogs["en"].get(key))
                self.assertTrue(catalogs["es"].get(key))

        for locale, catalog in catalogs.items():
            outcomes = [catalog[f"chapter.{number}.outcome"] for number in range(11)]
            proofs = [catalog[f"chapter.{number}.proof"] for number in range(11)]
            prompts = [catalog[f"lab.{number}.prompt"] for number in range(11)]
            self.assertEqual(len(set(outcomes)), 11, locale)
            self.assertEqual(len(set(proofs)), 11, locale)
            self.assertEqual(len(set(prompts)), 11, locale)
            for stage in ("overview", "build", "test", "reflect", "complete"):
                self.assertTrue(catalog.get(f"flow.guide.detail.{stage}"), (locale, stage))
                for step in range(1, 4):
                    self.assertTrue(catalog.get(f"flow.check.{stage}.{step}"), (locale, stage, step))

    def test_navigation_links_target_real_sections(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        targets = set(re.findall(r'\bid="([^"]+)"', html))
        internal_links = re.findall(r'href="#([^"]+)"', html)

        self.assertTrue(internal_links)
        self.assertTrue(set(internal_links).issubset(targets))

    def test_every_chapter_requires_distinct_lab_evidence(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        for number in range(11):
            self.assertRegex(script, rf"\b{number}: \[[^\]]+\]")
        self.assertGreaterEqual(script.count('["built",'), 11)
        self.assertGreaterEqual(script.count('"reflected"'), 14)
        self.assertGreaterEqual(script.count('"predicted"'), 13)
        self.assertIn('10: ["built", "predicted", "completed", "insufficient", "reflected"]', script)
        self.assertIn("completeChapter()", script)
        self.assertIn("recordLabEvidence", script)

    def test_every_chapter_has_three_construction_steps_and_a_guided_challenge(self) -> None:
        workshop = (ROOT / "web" / "workshop.js").read_text(encoding="utf-8")
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")

        self.assertIn("window.WORKSHOP_CHAPTERS", workshop)
        self.assertEqual(workshop.count("files: ["), 11)
        self.assertEqual(workshop.count("answer:"), 11)
        self.assertEqual(workshop.count("steps: ["), 22)
        self.assertIn('id="workshop-code"', html)
        self.assertIn('id="workshop-command"', html)
        self.assertIn('id="workshop-output"', html)
        self.assertIn('id="workshop-answer-options"', html)
        self.assertIn('id="workshop-challenge-code"', html)
        self.assertNotIn('id="workshop-answer"', html)

    def test_guided_choices_replace_prediction_and_reflection_typing(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        study = (ROOT / "web" / "study-content.js").read_text(encoding="utf-8")

        self.assertIn('id="reflection-options"', html)
        self.assertNotIn('id="reflection-answer"', html)
        self.assertNotIn('id="prediction-answer"', script)
        self.assertIn('name="prediction-choice"', script)
        self.assertIn('name="reflection-choice"', script)
        self.assertEqual(study.count("icon:"), 11)
        self.assertEqual(study.count("prediction:"), 22)
        self.assertEqual(study.count("reflection:"), 22)

    def test_paula_opens_a_chapter_specific_technical_notebook(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        catalogs = {
            locale: json.loads(
                (ROOT / "src" / "agent_atelier" / "locales" / f"{locale}.json").read_text(
                    encoding="utf-8"
                )
            )
            for locale in ("en", "es")
        }

        self.assertIn('id="paula-details"', html)
        self.assertIn('id="paula-details-panel"', html)
        self.assertIn('role="dialog"', html)
        self.assertIn('aria-modal="true"', html)
        self.assertIn('aria-labelledby="paula-details-title"', html)
        self.assertIn('id="paula-detail-steps"', html)
        self.assertIn('id="paula-detail-summary"', html)
        self.assertIn("function renderPaulaDetails()", script)
        self.assertIn("content.plain", script)
        self.assertIn("content.example", script)
        self.assertIn("content.pitfall", script)
        self.assertIn("copy.steps.map", script)
        self.assertIn("function togglePaulaDetails()", script)
        self.assertIn("closePaulaDetails(true)", script)
        self.assertIn('setAttribute("title", t("paula.details.open"))', script)
        for catalog in catalogs.values():
            for key in (
                "paula.details.open",
                "paula.details.connection",
                "paula.details.summary_template",
                "prediction.saved_detail",
                "reflection.success_detail",
                "reflection.incorrect_detail",
            ):
                self.assertTrue(catalog.get(key), key)

    def test_question_feedback_teaches_the_reason_not_only_the_score(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn('t("prediction.saved_detail"', script)
        self.assertIn('t("reflection.success_detail"', script)
        self.assertIn('t("reflection.incorrect_detail"', script)
        self.assertIn("correctText", script)

    def test_study_mode_and_animated_reward_are_packaged(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertIn('id="study-link"', html)
        self.assertIn('id="study-chapters"', html)
        self.assertIn("function renderStudyMode()", script)
        self.assertIn("launchCelebrationConfetti", script)
        self.assertIn("confetti-fall", css)
        for name in ("paula-trophy.gif", "indy-trophy.gif"):
            asset = ROOT / "assets" / "characters" / "celebration" / name
            self.assertTrue(asset.is_file() and asset.stat().st_size > 10_000)

    def test_learning_and_workshop_modes_are_materially_different(self) -> None:
        css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("body.compact", css)
        self.assertIn(".chapter-path", css)
        self.assertIn(".learning-brief", css)
        self.assertIn("localStorage.setItem(\"agent-atelier-mode\"", script)

    def test_chapters_use_a_guided_five_stage_journey(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertEqual(html.count("data-journey-stage="), 5)
        self.assertIn('id="guide-action"', html)
        self.assertIn("function renderJourney()", script)
        self.assertIn("function followGuideAction()", script)
        self.assertIn('[data-phase="build"]', css)
        self.assertIn('[data-phase="test"]', css)

    def test_original_pixel_studio_background_is_integrated_and_tracked(self) -> None:
        background = ROOT / "assets" / "backgrounds" / "cozy-pixel-studio-v1.png"
        css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
        asset_credits = (ROOT / "ASSET_CREDITS.md").read_text(encoding="utf-8")

        self.assertTrue(background.is_file() and background.stat().st_size > 100_000)
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        self.assertIn("cozy-pixel-studio-v1.png", css)
        self.assertIn("body::before", css)
        self.assertNotIn('class="studio-hero"', html)
        self.assertIn("cozy-pixel-studio-v1.png", asset_credits)

    def test_primary_palette_is_dark_blue_with_pink_as_secondary_accent(self) -> None:
        tokens = json.loads((ROOT / "design" / "tokens.json").read_text(encoding="utf-8"))

        self.assertEqual(tokens["color"]["canvas"]["deep"], "#081426")
        self.assertEqual(tokens["color"]["surface"]["panel"], "#10223B")
        self.assertEqual(tokens["color"]["accent"]["sky"], "#6EBBFF")
        self.assertNotEqual(tokens["color"]["accent"]["pink"], "#D16BA5")

    def test_transparent_character_stills_are_connected_to_progressive_studio(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn('data-character="paula"', html)
        self.assertIn('data-character="indy"', html)
        self.assertIn('id="paula-image"', html)
        self.assertIn('id="indy-image"', html)
        self.assertIn('class="sidebar-indy"', html)
        self.assertIn("indy-resting.png", html)
        self.assertIn("studio-props", html)
        self.assertIn('id="guide-checklist"', html)
        self.assertIn('id="character-pose-note"', html)
        self.assertIn("document.body.dataset.chapter", script)
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertIn("animation: none !important", css)
        self.assertNotIn("paula-indy-coarse-pixel-sheet-v2.png", css)
        self.assertNotIn("background-position", "\n".join(line for line in css.splitlines() if ".paula" in line or ".indy" in line))
        self.assertIn("function preloadCharacterImages()", script)
        self.assertIn("function setCharacterImage(", script)
        self.assertIn('setCharacterImage("#paula-image", "paula", currentChapter)', script)
        self.assertIn('setCharacterImage("#indy-image", "indy", currentChapter)', script)
        self.assertIn("candidate.addEventListener(\"error\"", script)
        self.assertIn('id="indy-help"', html)
        self.assertIn('id="indy-help-panel"', html)
        self.assertIn('id="indy-reveal-answer"', html)
        self.assertIn("function toggleIndyHelp()", script)
        self.assertIn("function toggleIndyAnswer()", script)

        for character in ("paula", "indy"):
            files = sorted((ROOT / "assets" / "characters" / character).glob("chapter-*.png"))
            self.assertEqual(len(files), 11)
            hashes = set()
            for image in files:
                payload = image.read_bytes()
                self.assertEqual(payload[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(payload[25], 6, f"{image.name} must use RGBA transparency")
                hashes.add(hashlib.sha256(payload).hexdigest())
            self.assertEqual(len(hashes), 11)

        sidebar_indy = ROOT / "assets" / "characters" / "sidebar" / "indy-resting.png"
        self.assertTrue(sidebar_indy.is_file() and sidebar_indy.stat().st_size > 1_000)
        self.assertIn("center center / cover no-repeat", css)

    def test_sleeping_mascot_and_completion_reward_are_real_progress_features(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn('name="application-name" content="Agent Atelier"', html)
        self.assertIn('id="completion-celebration"', html)
        self.assertIn('id="celebration-replay"', html)
        self.assertIn('id="creator-links"', html)
        self.assertIn("@keyframes indy-breathe", css)
        self.assertIn("@keyframes indy-sleep-z", css)
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertIn("completedChapters.size === 11", script)
        self.assertIn("function showCompletionCelebration", script)
        self.assertIn('linkedin: "https://www.linkedin.com/in/paula-garcia-fernandez-pgf3712"', script)
        self.assertIn('github: "https://github.com/pgf3712"', script)

    def test_optional_audio_is_original_procedural_and_user_controlled(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        audio = (ROOT / "web" / "audio.js").read_text(encoding="utf-8")
        licenses = (ROOT / "assets" / "audio" / "LICENSES.md").read_text(encoding="utf-8")

        self.assertIn('id="audio-toggle"', html)
        self.assertIn('id="audio-volume"', html)
        self.assertIn('src="audio.js?v=4"', html)
        self.assertIn('id="ambient-track"', html)
        self.assertIn('agent-atelier-ambient.wav?v=2', html)
        self.assertIn("window.AudioContext", audio)
        self.assertIn('toggle.addEventListener("click", toggleAudio)', audio)
        self.assertIn("agent-atelier-audio-volume", audio)
        self.assertIn('track.controls = true', audio)
        self.assertNotIn("autoplay", html.lower())
        self.assertIn("No third-party audio files are included", licenses)
        wav = ROOT / "assets" / "audio" / "agent-atelier-ambient.wav"
        self.assertTrue(wav.is_file() and wav.stat().st_size > 1_000_000)
        self.assertEqual(wav.read_bytes()[:4], b"RIFF")

    def test_completion_control_and_safe_provider_launcher_are_explicit(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn('id="completion-short-status"', html)
        self.assertIn('id="reset-progress-dialog"', html)
        self.assertIn('id="reset-progress"', html)
        self.assertIn("function nextCompletionRequirement()", script)
        self.assertIn("function resetCourseProgress()", script)
        self.assertNotIn('id="provider-api-key"', script)
        self.assertNotIn("requestBody.api_key", script)
        self.assertIn("provider.safe_launcher", script)
        preview = (ROOT / "src" / "agent_atelier" / "preview.py").read_text(encoding="utf-8")
        self.assertIn('if "api_key" in payload:', preview)
        self.assertIn("Credentials are not accepted from the browser", preview)
        launcher = ROOT / "OPEN_AGENT_ATELIER_REAL.bat"
        secure_script = ROOT / "scripts" / "start_real_provider.ps1"
        self.assertTrue(launcher.is_file())
        self.assertTrue(secure_script.is_file())
        secure_text = secure_script.read_text(encoding="utf-8")
        self.assertIn("-AsSecureString", secure_text)
        self.assertIn("Remove-Item Env:OPENAI_API_KEY", secure_text)
