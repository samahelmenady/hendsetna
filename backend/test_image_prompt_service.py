import unittest
from urllib.parse import unquote

from image_prompt_service import build_pollinations_safe_prompt, generate_design_image


class PollinationsSafePromptTest(unittest.TestCase):
    """Tests for build_pollinations_safe_prompt and generate_design_image."""

    def _make_concept(self, **overrides):
        """Return a minimal concept dict for use in tests."""
        base = {
            "space_type": "living room",
            "style_direction": "Modern Luxury",
            "mood": "Calm",
            "preferred_colors": ["blue", "white", "light wood"],
            "colors_to_avoid": ["red", "black"],
            "materials": [
                {"name": "wood"},
                {"name": "fabric"},
                {"name": "glass"},
            ],
            "furniture_suggestions": [
                "comfortable sofa",
                "coffee table",
                "TV wall",
                "storage unit",
            ],
            "lighting_suggestions": [
                "warm hidden LED",
                "medium natural light",
                "pendant lights",
            ],
            "image_generation_prompt": "",
            "negative_prompt": "",
        }
        base.update(overrides)
        return base

    def _make_user_data(self, **overrides):
        """Return a minimal user_data dict for use in tests."""
        base = {
            "project_name": "Blue Lounge",
            "project_type": "residential",
            "space_type": "living room",
            "personal_inspiration": None,
        }
        base.update(overrides)
        return base

    def test_safe_prompt_is_short_english_and_keeps_core_constraints(self):
        concept = self._make_concept()
        user_data = self._make_user_data()

        safe_prompt = build_pollinations_safe_prompt(concept, user_data, max_chars=600)

        self.assertLessEqual(len(safe_prompt), 600)
        self.assertTrue(safe_prompt.isascii())

        # Core style and mood
        self.assertIn("Modern Luxury", safe_prompt)
        self.assertIn("Calm", safe_prompt)

        # Quality markers
        self.assertIn("photorealistic", safe_prompt.lower())
        self.assertIn("wide-angle", safe_prompt.lower())
        self.assertIn("architectural visualization", safe_prompt.lower())
        self.assertIn("no people", safe_prompt.lower())

    def test_safe_prompt_includes_preferred_colors(self):
        concept = self._make_concept()
        user_data = self._make_user_data()

        safe_prompt = build_pollinations_safe_prompt(concept, user_data)

        self.assertIn("blue", safe_prompt.lower())
        self.assertIn("white", safe_prompt.lower())
        self.assertIn("light wood", safe_prompt.lower())

    def test_safe_prompt_includes_avoided_colors(self):
        concept = self._make_concept()
        user_data = self._make_user_data()

        safe_prompt = build_pollinations_safe_prompt(concept, user_data)

        self.assertIn("red", safe_prompt.lower())
        self.assertIn("black", safe_prompt.lower())

    def test_generate_design_image_returns_expected_keys(self):
        """generate_design_image should always return the required keys."""
        concept = self._make_concept(
            image_generation_prompt=(
                "Photorealistic interior design render of a living room, "
                "Modern Luxury style, Calm atmosphere, blue and white palette."
            ),
            negative_prompt="distorted furniture, watermark",
        )
        user_data = self._make_user_data()

        result = generate_design_image(concept, user_data)

        for key in (
            "image_generation_status",
            "image_provider",
            "image_url",
            "image_url_prompt",
        ):
            self.assertIn(key, result)

        self.assertEqual(result["image_provider"], "pollinations")
        self.assertIsNotNone(result["image_url"])
        # The prompt used in the URL must be within the safe-prompt length limit
        if result.get("image_url_prompt"):
            self.assertLessEqual(len(result["image_url_prompt"]), 900)


if __name__ == "__main__":
    unittest.main()
