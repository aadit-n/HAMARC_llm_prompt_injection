import json
import tempfile
import unittest
from pathlib import Path

from app import (
    GameConfig,
    Secret,
    build_system_prompt,
    find_disclosures,
    normalized,
    visible_model_output,
)


class DetectorTests(unittest.TestCase):
    def setUp(self):
        self.secrets = (
            Secret("code", "Codename", "NIGHTJAR"),
            Secret("place", "Location", "DOCK 17"),
            Secret("time", "Time", "03:10"),
        )

    def test_normalizes_case_and_formatting(self):
        self.assertEqual(normalized("N-I-G-H-T J.A.R"), "nightjar")

    def test_finds_disclosures_with_formatting(self):
        text = "The place is Dock-17 and the time is 03 10."
        self.assertEqual(find_disclosures(text, self.secrets), {"place", "time"})

    def test_does_not_match_absent_secret(self):
        self.assertEqual(find_disclosures("I know nothing.", self.secrets), set())

    def test_strips_model_reasoning(self):
        raw = "Private reasoning containing NIGHTJAR.</think>\nI know nothing."
        visible = visible_model_output(raw)
        self.assertEqual(visible, "I know nothing.")
        self.assertEqual(find_disclosures(visible, self.secrets), set())


class ConfigTests(unittest.TestCase):
    def test_rejects_empty_secret_list(self):
        raw = {
            "title": "Game",
            "model": "model",
            "max_prompts": 3,
            "assistant_name": "Guard",
            "player_briefing": "Brief",
            "plot_template": "Plot",
            "guard_instructions": "Guard",
            "secrets": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "game.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "At least one secret"):
                GameConfig.load(path)

    def test_system_prompt_contains_dossier(self):
        config = GameConfig(
            title="Game",
            model="model",
            max_prompts=3,
            temperature=0.7,
            assistant_name="Guard",
            player_briefing="Brief",
            plot_template="Plot",
            guard_instructions="Keep it safe.",
            secrets=(Secret("code", "Codename", "NIGHTJAR"),),
        )
        prompt = build_system_prompt(config)
        self.assertIn("Codename: NIGHTJAR", prompt)
        self.assertIn("Keep it safe.", prompt)


if __name__ == "__main__":
    unittest.main()
