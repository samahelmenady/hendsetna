import base64
import random
import re
import unicodedata
from urllib.parse import quote

import requests

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt"
PROMPT_QUALITY_INSTRUCTION = (
    "Photorealistic interior design render, high-end architectural visualization, "
    "realistic proportions, wide-angle interior photography, professional lighting, "
    "balanced composition, clean realistic interior styling, no people."
)
POLLINATIONS_FALLBACK_PROMPT = (
    "photorealistic modern bedroom interior design, blue and white color palette, "
    "light wood furniture, bed, desk, chair, wall art paintings, relaxing warm LED "
    "lighting, inspired by the sea, high-end architectural visualization, wide-angle "
    "interior photography, realistic proportions, no people"
)
ARABIC_DESIGN_TRANSLATIONS = {
    "مستوحى من البحر": "inspired by the sea",
    "إضاءة للاسترخاء": "relaxing warm lighting",
    "إضاءة هادئة": "soft relaxing lighting",
    "غرفة معيشة": "living room",
    "صالون": "living room",
    "غرفة نوم": "bedroom",
    "مطبخ": "kitchen",
    "حمام": "bathroom",
    "ازرق": "blue", "أزرق": "blue",
    "احمر": "red", "أحمر": "red",
    "ابيض": "white", "أبيض": "white",
    "بيج": "beige",
    "خشب": "wood",
    "خشب فاتح": "light wood",
    "فاتح": "light",
    "سرير": "bed",
    "مكتب": "desk",
    "كرسي": "chair",
    "كنبة": "sofa",
    "طاولة": "table",
    "لوحات": "wall art paintings",
    "البحر": "sea",
    "فندق": "hotel",
    "فاخر": "luxury",
    "مودرن": "modern",
}


def _flatten_to_text(value):
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, list):
        return ", ".join(_flatten_to_text(item) for item in value if _flatten_to_text(item))
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            text = _flatten_to_text(item)
            if text:
                parts.append(f"{key}: {text}")
        return ", ".join(parts)
    return str(value).strip()


def _join_terms(terms):
    terms = [term for term in terms if term]
    if not terms:
        return ""
    if len(terms) == 1:
        return terms[0]
    return ", ".join(terms[:-1]) + f" and {terms[-1]}"


def build_negative_prompt():
    """Shared negative prompt for image model integrations."""
    return (
        "distorted furniture, unrealistic proportions, cluttered layout, bad lighting, "
        "extra doors, extra windows, low quality render, cartoon style, messy layout, "
        "warped perspective, duplicate objects, unusable circulation, overdecorated space, "
        "blurry image, watermark, text, logo overload, cluttered space"
    )


def required_response_schema():
    return {
        "project_type": "string",
        "space_type": "string",
        "design_brief": "string",
        "concept_summary": "string",
        "style_direction": "string",
        "mood": "string",
        "color_palette": [
            {
                "name": "string",
                "hex": "string",
                "usage": "string",
            }
        ],
        "materials": [
            {
                "name": "string",
                "usage": "string",
            }
        ],
        "furniture_suggestions": ["string"],
        "lighting_suggestions": ["string"],
        "layout_suggestions": ["string"],
        "image_generation_prompt": "string",
        "negative_prompt": "string",
    }


def _has_quality_instruction(prompt):
    lowered = prompt.lower()
    return all(
        term in lowered
        for term in ("photorealistic", "architectural visualization", "wide-angle")
    )


def _finalize_pollinations_prompt(image_prompt: str, negative_prompt: str = "") -> str:
    final_prompt = (image_prompt or "").strip()
    if not final_prompt:
        raise ValueError("No image prompt was provided.")

    if not _has_quality_instruction(final_prompt):
        final_prompt = f"{final_prompt} {PROMPT_QUALITY_INSTRUCTION}"

    if negative_prompt and negative_prompt.strip():
        final_prompt = f"{final_prompt} Avoid: {negative_prompt.strip()}."

    return final_prompt


def _ascii_only(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", ascii_text).strip()


def _translate_arabic_design_terms(text: str) -> str:
    translated = text or ""
    for arabic, english in sorted(
        ARABIC_DESIGN_TRANSLATIONS.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        translated = translated.replace(arabic, f" {english} ")
    return re.sub(r"\s+", " ", translated).strip()


def _strip_upload_placeholders(text: str) -> str:
    patterns = (
        r"uploads?:\s*[^.]*placeholder[^.]*\.",
        r"upload ui exists[^.]*\.",
        r"imagesprovided:\s*[^.]*\.",
        r"status:\s*placeholder_only[^.]*\.",
        r"raw upload[^.]*\.",
    )
    cleaned = text
    for pattern in patterns:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)
    return cleaned


def _trim_to_sentence_boundary(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    trimmed = text[:max_chars].rsplit(" ", 1)[0].strip(" ,;:-")
    sentence_end = max(trimmed.rfind("."), trimmed.rfind(";"))
    if sentence_end > max_chars * 0.65:
        trimmed = trimmed[:sentence_end + 1]
    return trimmed.strip()


def build_pollinations_safe_prompt(concept: dict, user_data: dict, max_chars: int = 600) -> str:
    def _translate(text_value):
        return _translate_arabic_design_terms(str(text_value or "")).strip()

    space_type = _translate(concept.get("space_type"))
    style = _translate(concept.get("style_direction"))
    mood = _translate(concept.get("mood"))

    preferred_colors = [_translate(c) for c in concept.get("preferred_colors", [])]
    colors_to_avoid = [_translate(c) for c in concept.get("colors_to_avoid", [])]

    materials_list = concept.get("materials", [])
    if materials_list and isinstance(materials_list[0], dict):
        materials = [_translate(m.get("name")) for m in materials_list]
    else:
        materials = [_translate(m) for m in materials_list]

    furniture = _translate(_flatten_to_text(concept.get("furniture_suggestions")))
    lighting = _translate(_flatten_to_text(concept.get("lighting_suggestions")))
    inspiration = _translate(user_data.get("personal_inspiration"))

    prompt_parts = [f"Photorealistic interior design render of a {space_type}"]
    if style:
        prompt_parts.append(f"{style} style")
    if mood:
        prompt_parts.append(f"{mood} atmosphere")

    color_parts = []
    if preferred_colors:
        color_parts.append(f"color palette: {_join_terms(preferred_colors)}")
    if colors_to_avoid:
        color_parts.append(f"avoid using {_join_terms(colors_to_avoid)}")
    if color_parts:
        prompt_parts.append(", ".join(color_parts))

    if materials:
        prompt_parts.append(f"materials: {_join_terms(materials)}")
    if furniture:
        prompt_parts.append(f"furniture: {furniture}")
    if lighting:
        prompt_parts.append(f"lighting: {lighting}")
    if inspiration:
        prompt_parts.append(f"inspired by {inspiration}, translated into a tasteful interior design concept")

    quality_words = (
        "high-end architectural visualization, wide-angle interior photography, "
        "realistic proportions, balanced composition, professional lighting, "
        "clean interior styling, no people, no text, no watermark"
    )

    safe_prompt = ", ".join(p.strip(" .,") for p in prompt_parts if p and p.strip(" .,"))
    safe_prompt = f"{safe_prompt}, {quality_words}"
    safe_prompt = _ascii_only(safe_prompt)
    safe_prompt = re.sub(r"\s+", " ", safe_prompt).strip()

    if len(safe_prompt) < 50:
        return POLLINATIONS_FALLBACK_PROMPT

    return _trim_to_sentence_boundary(safe_prompt, max_chars)


def generate_design_image(concept: dict, user_data: dict) -> dict:
    image_url = None
    image_url_prompt = None
    try:
        image_generation_prompt = concept.get("image_generation_prompt", "")
        negative_prompt = concept.get("negative_prompt", "")

        final_prompt_for_log = _finalize_pollinations_prompt(image_generation_prompt, negative_prompt)
        image_url_prompt = build_pollinations_safe_prompt(concept, user_data)

        encoded_prompt = quote(image_url_prompt, safe="")
        seed = random.randint(1, 999999999)
        image_url = (
            f"{POLLINATIONS_BASE_URL}/{encoded_prompt}"
            f"?width=768&height=768&nologo=true&enhance=true&seed={seed}"
        )

        print("Using image provider: pollinations")
        print("Final image prompt preview:", final_prompt_for_log[:800])
        print("FINAL image_url_prompt:", image_url_prompt)
        print("Contains non-ascii:", any(ord(c) > 127 for c in image_url_prompt))
        print("Pollinations safe prompt length:", len(image_url_prompt))
        print("Pollinations URL length:", len(image_url))
        print("Image URL generated:", bool(image_url))

        # Fetch the image from the URL
        print("Fetching Pollinations image from URL...")
        response = requests.get(image_url, timeout=90)
        print("Pollinations fetch status:", response.status_code)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx status

        content_type = response.headers.get("Content-Type")
        print("Pollinations content type:", content_type)

        if not (content_type and content_type.startswith("image/")):
            raise ValueError(
                f"Expected an image from Pollinations, but received content type: {content_type}"
            )

        image_base64 = base64.b64encode(response.content).decode("utf-8")
        print("Image base64 generated:", bool(image_base64))

        return {
            "image_generation_status": "success",
            "image_provider": "pollinations",
            "image_url": image_url,
            "image_url_prompt": image_url_prompt,
            "image_base64": image_base64,
            "image_mime_type": content_type,
        }
    except Exception as exc:
        error_message = str(exc)
        if image_url:
            error_message = f"Pollinations URL was generated, but backend could not download the image: {exc}"

        print("Image generation or fetch failed:", error_message)

        return {
            "image_generation_status": "failed",
            "image_provider": "pollinations",
            "image_url": image_url,
            "image_url_prompt": image_url_prompt,
            "image_base64": None,
            "image_mime_type": None,
            "image_generation_error": error_message,
        }
