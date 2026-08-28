import unittest
from unittest.mock import patch

import app as app_module
from gemini_service import build_fallback_design_concept, normalize_user_payload


class FallbackConceptTest(unittest.TestCase):
    def setUp(self):
        self.raw_payload = {
            "projectType": "residential",
            "projectName": "Blue Lounge",
            "spaceType": "living room",
            "preferredColors": "blue, white, light wood",
            "colorsToAvoid": "red, black",
            "interiorStyle": "Modern Luxury",
            "mood": "Calm",
            "materials": ["wood", "fabric", "glass"],
            "furnitureRequirements": "comfortable sofa, coffee table, TV wall, storage unit",
            "lighting": "warm hidden LED, medium natural light, pendant lights",
        }
        self.user_data = normalize_user_payload(self.raw_payload)

    def test_fallback_concept_includes_required_user_inputs(self):
        concept = build_fallback_design_concept(self.user_data)
        prompt = concept.get("image_generation_prompt", "")
        negative_prompt = concept.get("negative_prompt", "")

        # Preferred colors should appear in the prompt
        self.assertIn("blue", prompt.lower())
        self.assertIn("white", prompt.lower())
        self.assertIn("light wood", prompt.lower())

        # Avoided colors should appear in the negative prompt
        self.assertIn("red", negative_prompt.lower())
        self.assertIn("black", negative_prompt.lower())

        # Style and mood
        self.assertIn("Modern Luxury", prompt)
        self.assertIn("Calm", prompt)

        # Quality markers
        self.assertIn("photorealistic", prompt.lower())
        self.assertIn("no people", prompt.lower())

    def test_fallback_concept_has_required_fields(self):
        concept = build_fallback_design_concept(self.user_data)
        self.assertTrue(concept.get("success"))
        self.assertEqual(concept.get("concept_generation_status"), "fallback_used")
        self.assertIsInstance(concept.get("color_palette"), list)
        self.assertIsInstance(concept.get("materials"), list)
        self.assertIsInstance(concept.get("furniture_suggestions"), list)
        self.assertIsInstance(concept.get("lighting_suggestions"), list)
        self.assertIsInstance(concept.get("preferred_colors"), list)
        self.assertIsInstance(concept.get("colors_to_avoid"), list)

    def test_endpoint_uses_fallback_when_gemini_is_unavailable(self):
        image_url = "https://image.pollinations.ai/prompt/fallback"

        with patch(
            "app.generate_design_concept",
            return_value={
                "success": False,
                "error_type": "gemini_unavailable",
                "error": "Gemini is temporarily unavailable.",
            },
        ), patch(
            "app.generate_design_image",
            return_value={
                "image_generation_status": "success",
                "image_provider": "pollinations",
                "image_url": image_url,
                "image_base64": None,
                "image_mime_type": None,
            },
        ):
            client = app_module.app.test_client()
            response = client.post(
                "/api/generate-design", json=self.raw_payload
            )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("concept_generation_status"), "fallback_used")
        self.assertEqual(data.get("image_generation_status"), "success")
        self.assertEqual(data.get("image_url"), image_url)

    def test_endpoint_uses_fallback_when_gemini_returns_invalid_json(self):
        image_url = "https://image.pollinations.ai/prompt/fallback-invalid-json"

        with patch(
            "app.generate_design_concept",
            return_value={
                "success": False,
                "error_type": "gemini_invalid_json",
                "error": "Gemini returned invalid JSON. Using fallback prompt.",
                "details": "Expecting property name enclosed in double quotes",
            },
        ), patch(
            "app.generate_design_image",
            return_value={
                "image_generation_status": "success",
                "image_provider": "pollinations",
                "image_url": image_url,
                "image_url_prompt": "safe fallback prompt",
                "image_base64": None,
                "image_mime_type": None,
            },
        ):
            client = app_module.app.test_client()
            response = client.post(
                "/api/generate-design", json=self.raw_payload
            )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("concept_generation_status"), "fallback_used")
        self.assertEqual(data.get("image_generation_status"), "success")
        self.assertEqual(data.get("image_url"), image_url)


if __name__ == "__main__":
    unittest.main()
