import unittest
from unittest.mock import patch

import app as app_module


class FallbackImagePromptTest(unittest.TestCase):
    def setUp(self):
        self.payload = app_module._normalize_keys({
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
        })

    def test_fallback_prompt_includes_required_user_inputs(self):
        prompt_data = app_module.build_fallback_image_prompt(self.payload)
        prompt = prompt_data["image_generation_prompt"]
        negative_prompt = prompt_data["negative_prompt"]

        for required_text in (
            "blue, white, light wood",
            "Avoid red and black",
            "Modern Luxury",
            "Calm",
            "wood, fabric, glass",
            "comfortable sofa, coffee table, TV wall, storage unit",
            "Lighting details: warm hidden LED, medium natural light, pendant lights",
            "photorealistic interior design render",
            "High-end architectural visualization",
            "wide-angle interior photography",
            "realistic proportions",
            "no people",
        ):
            self.assertIn(required_text, prompt)

        for required_text in (
            "avoid red and black",
            "distorted furniture",
            "unrealistic proportions",
            "messy layout",
            "low quality",
            "blurry",
            "cartoon style",
            "watermark",
            "text",
            "logo overload",
            "cluttered space",
        ):
            self.assertIn(required_text, negative_prompt)

    def test_endpoint_uses_fallback_prompt_when_gemini_is_unavailable(self):
        image_url = "https://image.pollinations.ai/prompt/fallback"

        with patch.object(app_module, "generate_design_concept", return_value={
            "success": False,
            "error_type": "gemini_unavailable",
        }), patch.object(app_module, "generate_design_image", return_value={
            "image_generation_status": "success",
            "image_provider": "pollinations",
            "image_url": image_url,
            "image_base64": None,
            "image_mime_type": None,
        }) as image_mock:
            client = app_module.app.test_client()
            response = client.post("/api/generate-design", json=self.payload)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["concept_generation_status"], "fallback_used")
        self.assertEqual(data["image_generation_status"], "success")
        self.assertEqual(data["image_provider"], "pollinations")
        self.assertEqual(data["image_url"], image_url)

        fallback_prompt_arg = image_mock.call_args.args[0]
        self.assertTrue(fallback_prompt_arg)
        self.assertIn("blue, white, light wood", fallback_prompt_arg)
        self.assertIn("Avoid red and black", fallback_prompt_arg)

    def test_endpoint_uses_fallback_prompt_when_gemini_returns_invalid_json(self):
        image_url = "https://image.pollinations.ai/prompt/fallback-invalid-json"

        with patch.object(app_module, "generate_design_concept", return_value={
            "success": False,
            "error_type": "gemini_invalid_json",
            "error": "Gemini returned invalid JSON. Using fallback prompt.",
            "details": "Expecting property name enclosed in double quotes",
        }), patch.object(app_module, "generate_design_image", return_value={
            "image_generation_status": "success",
            "image_provider": "pollinations",
            "image_url": image_url,
            "image_url_prompt": "safe fallback prompt",
            "image_base64": None,
            "image_mime_type": None,
        }) as image_mock:
            client = app_module.app.test_client()
            response = client.post("/api/generate-design", json=self.payload)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["concept_generation_status"], "fallback_used")
        self.assertEqual(data["image_generation_status"], "success")
        self.assertEqual(data["image_provider"], "pollinations")
        self.assertEqual(data["image_url"], image_url)
        self.assertEqual(data["image_url_prompt"], "safe fallback prompt")
        self.assertIn("unavailable or invalid", data["concept_summary"])
        self.assertTrue(image_mock.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
