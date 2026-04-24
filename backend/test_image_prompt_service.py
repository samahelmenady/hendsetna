import unittest
from urllib.parse import unquote

from image_prompt_service import build_pollinations_safe_prompt, generate_design_image


class PollinationsSafePromptTest(unittest.TestCase):
    def test_safe_prompt_is_short_english_and_keeps_core_constraints(self):
        long_prompt = """
        Create a photorealistic interior design render for ط¨ط±ظˆط¬ظٹظƒطھ residential living room.
        Preferred color palette: blue, white, light wood.
        Avoid red and black.
        Interior style: Modern Luxury.
        Mood: Calm.
        Materials: wood, fabric, glass.
        Furniture requirements: comfortable sofa, coffee table, TV wall, storage unit.
        Lighting details: warm hidden LED, medium natural light, pendant lights.
        Uploads: status: placeholder_only, imagesProvided: false, note: Upload UI exists, but no image file was submitted.
        Mandatory user constraints: Selected materials: wood, fabric, glass. Furniture requirements:
        comfortable sofa, coffee table, TV wall, storage unit. Lighting setup: warm hidden LED,
        medium natural light, pendant lights.
        Avoid: distorted furniture, unrealistic proportions, messy layout, low quality, blurry,
        cartoon style, watermark, text, logo overload, cluttered space.
        """ * 4

        safe_prompt = build_pollinations_safe_prompt(long_prompt)

        self.assertLessEqual(len(safe_prompt), 900)
        self.assertTrue(safe_prompt.isascii())
        self.assertIn("blue, white, light wood", safe_prompt)
        self.assertIn("Avoid red and black", safe_prompt)
        self.assertIn("Modern Luxury", safe_prompt)
        self.assertIn("Calm", safe_prompt)
        self.assertIn("wood, fabric, glass", safe_prompt)
        self.assertIn("comfortable sofa, coffee table, TV wall, storage unit", safe_prompt)
        self.assertIn("Lighting details", safe_prompt)
        self.assertIn("photorealistic interior design render", safe_prompt)
        self.assertIn("wide-angle interior photography", safe_prompt)
        self.assertIn("high-end architectural visualization", safe_prompt)
        self.assertIn("realistic proportions", safe_prompt)
        self.assertIn("no people", safe_prompt)
        self.assertNotIn("placeholder_only", safe_prompt)
        self.assertNotIn("Upload UI exists", safe_prompt)

    def test_generate_design_image_uses_safe_prompt_for_url(self):
        full_prompt = (
            "Create a photorealistic interior design render. "
            "Preferred color palette: blue, white, light wood. "
            "Avoid red and black. Interior style: Modern Luxury. Mood: Calm. "
            "Materials: wood, fabric, glass. Furniture requirements: comfortable sofa, "
            "coffee table, TV wall, storage unit. Lighting details: warm hidden LED, "
            "medium natural light, pendant lights. "
        ) * 20

        result = generate_design_image(full_prompt, "distorted furniture, watermark")
        decoded_url_prompt = unquote(
            result["image_url"].split("/prompt/", 1)[1].split("?width=", 1)[0]
        )

        self.assertEqual(result["image_generation_status"], "success")
        self.assertEqual(result["image_provider"], "pollinations")
        self.assertIn("image_url_prompt", result)
        self.assertEqual(decoded_url_prompt, result["image_url_prompt"])
        self.assertLessEqual(len(result["image_url_prompt"]), 900)


if __name__ == "__main__":
    unittest.main()
