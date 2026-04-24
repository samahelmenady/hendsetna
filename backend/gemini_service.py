import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

try:
    from image_prompt_service import build_negative_prompt, required_response_schema
except ImportError:
    from .image_prompt_service import build_negative_prompt, required_response_schema


DEFAULT_TEXT_MODEL_NAME = "gemini-1.5-flash"
RETRY_DELAYS = (0, 2, 5)


KEY_ALIASES = {
    "projectName": "project_name",
    "projectType": "project_type",
    "spaceType": "space_type",
    "businessType": "business_type",
    "brandName": "brand_name",
    "brandColors": "brand_colors",
    "targetCustomers": "target_customers",
    "guestType": "target_guests",
    "ceilingHeight": "ceiling_height",
    "numUsers": "number_of_users",
    "condition": "current_condition",
    "currentCondition": "current_condition",
    "interiorStyle": "interior_style",
    "customStyle": "custom_style",
    "prefColors": "preferred_colors",
    "preferredColors": "preferred_colors",
    "avoidColors": "colors_to_avoid",
    "colorsToAvoid": "colors_to_avoid",
    "furniture": "furniture_requirements",
    "furnitureRequirements": "furniture_requirements",
    "inspiration": "personal_inspiration",
    "personalInspiration": "personal_inspiration",
    "workStyle": "work_style",
}


def _clean_value(value):
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped or stripped.lower() in {"undefined", "null", "none"}:
            return None
        return stripped
    if isinstance(value, list):
        cleaned = [_clean_value(item) for item in value]
        return [item for item in cleaned if item not in (None, "", [], {})]
    if isinstance(value, dict):
        cleaned = {key: _clean_value(val) for key, val in value.items()}
        return {key: val for key, val in cleaned.items() if val not in (None, "", [], {})}
    return value


def sanitize_payload(payload):
    cleaned = _clean_value(payload or {})
    return cleaned if isinstance(cleaned, dict) else {}


def normalize_user_payload(payload):
    cleaned = sanitize_payload(payload)
    normalized = {}

    for key, value in cleaned.items():
        normalized_key = KEY_ALIASES.get(key, key)
        if normalized_key in normalized and normalized[normalized_key] not in (None, "", [], {}):
            continue
        normalized[normalized_key] = value

    return sanitize_payload(normalized)


def _json_from_text(text):
    if not text:
        raise ValueError("Gemini returned an empty response.")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def _is_temporary_gemini_error(exc):
    message = str(exc).lower()
    temporary_markers = (
        "503",
        "unavailable",
        "429",
        "resource_exhausted",
        "timeout",
        "timed out",
        "service unavailable",
        "please try again later",
    )
    return any(marker in message for marker in temporary_markers)


def _gemini_unavailable_error(exc):
    return {
        "success": False,
        "error_type": "gemini_unavailable",
        "error": "Gemini is temporarily unavailable. Please try again in a few minutes.",
        "details": str(exc),
    }


def _gemini_invalid_json_error(exc):
    return {
        "success": False,
        "error_type": "gemini_invalid_json",
        "error": "Gemini returned invalid JSON. Using fallback prompt.",
        "details": str(exc),
    }


def _normalize_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [str(value)]


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


def _split_constraint_terms(value):
    text = _flatten_to_text(value)
    if not text:
        return []
    terms = re.split(r"[,;/|]+|\band\b", text, flags=re.IGNORECASE)
    return [term.strip() for term in terms if term.strip()]


def _join_terms(terms):
    terms = [term for term in terms if term]
    if not terms:
        return ""
    if len(terms) == 1:
        return terms[0]
    return ", ".join(terms[:-1]) + f" and {terms[-1]}"


def _contains_term(text, term):
    if not text or not term:
        return False
    return term.lower() in text.lower()


def _all_terms_present(text, terms):
    return all(_contains_term(text, term) for term in terms)


def _split_color_text(value):
    if not value:
        return []
    raw_parts = _split_constraint_terms(value)
    colors = []
    for part in raw_parts:
        color = str(part).strip()
        if color and color.lower() not in {"undefined", "null", "none", "not specified"}:
            colors.append(color)
    return colors


def _user_color_constraints(user_data):
    preferred = []
    for key in ("preferred_colors", "brand_colors", "inspiration_colors"):
        preferred.extend(_split_color_text(user_data.get(key)))

    avoid = []
    for key in ("colors_to_avoid",):
        avoid.extend(_split_color_text(user_data.get(key)))

    seen = set()
    preferred_unique = []
    for color in preferred:
        lowered = color.lower()
        if lowered not in seen:
            seen.add(lowered)
            preferred_unique.append(color)

    seen = set()
    avoid_unique = []
    for color in avoid:
        lowered = color.lower()
        if lowered not in seen:
            seen.add(lowered)
            avoid_unique.append(color)

    return preferred_unique, avoid_unique


def _constraint_values(user_data):
    return {
        "project type": _flatten_to_text(user_data.get("project_type")),
        "project name": _flatten_to_text(user_data.get("project_name")),
        "space type": _flatten_to_text(user_data.get("space_type") or user_data.get("business_type")),
        "style": _flatten_to_text(user_data.get("interior_style") or user_data.get("work_style")),
        "mood": _flatten_to_text(user_data.get("mood")),
        "materials": _split_constraint_terms(user_data.get("materials")),
        "furniture": _split_constraint_terms(user_data.get("furniture_requirements")),
        "lighting": _split_constraint_terms(user_data.get("lighting")),
        "zones": _split_constraint_terms(user_data.get("zones")),
        "personal inspiration": _flatten_to_text(user_data.get("personal_inspiration")),
        "custom style": _flatten_to_text(user_data.get("custom_style")),
        "area": _flatten_to_text(user_data.get("area")),
        "dimensions": _flatten_to_text(user_data.get("dimensions")),
        "ceiling height": _flatten_to_text(user_data.get("ceiling_height")),
        "current condition": _flatten_to_text(user_data.get("current_condition")),
        "target customers": _flatten_to_text(user_data.get("target_customers")),
        "target guests": _flatten_to_text(user_data.get("target_guests")),
        "brand": _flatten_to_text({
            "brand_name": user_data.get("brand_name"),
            "brand_colors": user_data.get("brand_colors"),
            "company": user_data.get("company"),
        }),
        "uploads": _flatten_to_text(user_data.get("uploads")),
    }


def _palette_has_color(palette, color):
    color_lower = color.lower()
    for item in palette:
        if not isinstance(item, dict):
            continue
        text = f"{item.get('name', '')} {item.get('usage', '')}".lower()
        if color_lower in text:
            return True
    return False


def _remove_avoided_palette_colors(data, colors_to_avoid):
    if not colors_to_avoid or not isinstance(data.get("color_palette"), list):
        return
    avoided = [color.lower() for color in colors_to_avoid]
    filtered = []
    for item in data["color_palette"]:
        if not isinstance(item, dict):
            continue
        text = f"{item.get('name', '')} {item.get('usage', '')}".lower()
        if any(color in text for color in avoided):
            continue
        filtered.append(item)
    data["color_palette"] = filtered


def _append_missing_suggestions(data, user_data):
    constraints = _constraint_values(user_data)
    for material in constraints["materials"]:
        if not any(_contains_term(_flatten_to_text(item), material) for item in data.get("materials", [])):
            data.setdefault("materials", []).append({
                "name": material,
                "usage": "User-selected material to be incorporated in the design.",
            })

    for furniture in constraints["furniture"]:
        if not any(_contains_term(item, furniture) for item in data.get("furniture_suggestions", [])):
            data.setdefault("furniture_suggestions", []).append(f"Include {furniture} as requested by the user.")

    for lighting in constraints["lighting"]:
        if not any(_contains_term(item, lighting) for item in data.get("lighting_suggestions", [])):
            data.setdefault("lighting_suggestions", []).append(f"Use {lighting} as part of the lighting setup.")


def _ensure_prompt_has_all_constraints(data, user_data):
    prompt = data.get("image_generation_prompt", "").strip()
    constraints = _constraint_values(user_data)
    preferred_colors, colors_to_avoid = _user_color_constraints(user_data)
    missing_lines = []

    if preferred_colors and not _all_terms_present(prompt, preferred_colors):
        missing_lines.append(f"Use {', '.join(preferred_colors)} as the core palette.")
    if colors_to_avoid and not _all_terms_present(prompt, colors_to_avoid):
        missing_lines.append(f"Avoid {_join_terms(colors_to_avoid)} color usage.")

    for label in ("project type", "project name", "space type", "style", "mood"):
        value = constraints[label]
        if value and not _contains_term(prompt, value):
            missing_lines.append(f"{label.title()}: {value}.")

    if constraints["materials"] and not _all_terms_present(prompt, constraints["materials"]):
        missing_lines.append(f"Selected materials: {', '.join(constraints['materials'])}.")
    if constraints["furniture"] and not _all_terms_present(prompt, constraints["furniture"]):
        missing_lines.append(f"Include furniture requirements: {', '.join(constraints['furniture'])}.")
    if constraints["lighting"] and not _all_terms_present(prompt, constraints["lighting"]):
        missing_lines.append(f"Use lighting setup: {', '.join(constraints['lighting'])}.")
    if constraints["zones"] and not _all_terms_present(prompt, constraints["zones"]):
        missing_lines.append(f"Layout zones: {', '.join(constraints['zones'])}.")

    for label in (
        "personal inspiration",
        "custom style",
        "area",
        "dimensions",
        "ceiling height",
        "current condition",
        "target customers",
        "target guests",
        "brand",
        "uploads",
    ):
        value = constraints[label]
        if value and not _contains_term(prompt, value):
            missing_lines.append(f"{label.title()}: {value}.")

    render_line = (
        "Photorealistic interior design render, high-end architectural visualization, "
        "wide-angle interior photography, realistic proportions, balanced composition, "
        "clean professional styling, no people unless explicitly requested."
    )
    if not _contains_term(prompt, "photorealistic"):
        missing_lines.append(render_line)

    if missing_lines:
        data["image_generation_prompt"] = (
            f"{prompt}\n\nMandatory user constraints: " + " ".join(missing_lines)
        ).strip()


def _enforce_design_constraints(data, user_data):
    preferred_colors, colors_to_avoid = _user_color_constraints(user_data)
    data["preferred_colors"] = preferred_colors
    data["colors_to_avoid"] = colors_to_avoid
    data["color_palette"] = data.get("color_palette") if isinstance(data.get("color_palette"), list) else []
    _remove_avoided_palette_colors(data, colors_to_avoid)

    for color in preferred_colors:
        if not _palette_has_color(data["color_palette"], color):
            data["color_palette"].append({
                "name": color,
                "hex": "#4A90E2" if "blue" in color.lower() else "#D8D1C7",
                "usage": "User-selected mandatory color, used tastefully as a main tone or accent.",
            })

    preferred_text = ", ".join(preferred_colors)
    avoid_text = ", ".join(colors_to_avoid)
    if preferred_text and preferred_text.lower() not in data.get("design_brief", "").lower():
        data["design_brief"] = (
            f"{data.get('design_brief', '').strip()} The design must include the user's selected colors: "
            f"{preferred_text}."
        ).strip()

    _append_missing_suggestions(data, user_data)
    _ensure_prompt_has_all_constraints(data, user_data)

    negative_parts = [data.get("negative_prompt") or build_negative_prompt()]
    if avoid_text:
        negative_parts.append(f"Avoid {_join_terms(colors_to_avoid)} color usage")
    negative_parts.append("watermark, text, logo overload, cluttered space")
    data["negative_prompt"] = ", ".join(part for part in negative_parts if part)
    return data


def _simple_color_hex(color):
    lowered = color.lower()
    color_map = {
        "blue": "#2F6FDB",
        "white": "#FFFFFF",
        "light wood": "#D8B98A",
        "wood": "#B8875B",
        "green": "#4F7D5A",
        "red": "#B3261E",
        "black": "#111111",
        "gold": "#C8A24A",
        "beige": "#E8DCCB",
        "cream": "#F4EAD8",
        "gray": "#9AA0A6",
        "grey": "#9AA0A6",
    }
    for key, hex_value in color_map.items():
        if key in lowered:
            return hex_value
    return "#D8D1C7"


def build_fallback_design_concept(user_data, gemini_error=None):
    constraints = _constraint_values(user_data)
    preferred_colors, colors_to_avoid = _user_color_constraints(user_data)
    color_text = ", ".join(preferred_colors) if preferred_colors else "not specified"
    avoid_text = _join_terms(colors_to_avoid)
    materials = constraints["materials"]
    furniture = constraints["furniture"]
    lighting = constraints["lighting"]
    style = constraints["style"] or "not specified"
    mood = constraints["mood"] or "not specified"
    project_type = constraints["project type"] or "interior design project"
    space_type = constraints["space type"] or "interior space"

    prompt_parts = [
        f"Create a photorealistic interior design render for a {project_type} {space_type}.",
        f"Project name: {constraints['project name']}." if constraints["project name"] else "",
        f"Style: {style}.",
        f"Mood: {mood}.",
        f"Mandatory color palette: {color_text}." if preferred_colors else "",
        f"Avoid {avoid_text} color usage." if colors_to_avoid else "",
        f"Selected materials: {', '.join(materials)}." if materials else "",
        f"Furniture requirements: {', '.join(furniture)}." if furniture else "",
        f"Lighting setup: {', '.join(lighting)}." if lighting else "",
        f"Layout zones: {', '.join(constraints['zones'])}." if constraints["zones"] else "",
        f"Area: {constraints['area']}." if constraints["area"] else "",
        f"Dimensions: {constraints['dimensions']}." if constraints["dimensions"] else "",
        f"Ceiling height: {constraints['ceiling height']}." if constraints["ceiling height"] else "",
        f"Current condition: {constraints['current condition']}." if constraints["current condition"] else "",
        f"Target customers: {constraints['target customers']}." if constraints["target customers"] else "",
        f"Target guests: {constraints['target guests']}." if constraints["target guests"] else "",
        f"Brand or company info: {constraints['brand']}." if constraints["brand"] else "",
        f"Personal inspiration: {constraints['personal inspiration']}." if constraints["personal inspiration"] else "",
        f"Custom style direction: {constraints['custom style']}." if constraints["custom style"] else "",
        "Translate any club, brand, series, person, or logo inspiration into subtle colors, mood, shapes, materials, or decor; do not overload the space with logos.",
        "Use realistic scale, practical circulation, balanced furniture proportions, clean professional styling, wide-angle interior photography, high-end architectural visualization, no people.",
    ]

    negative_parts = [build_negative_prompt()]
    if colors_to_avoid:
        negative_parts.append(f"Avoid {avoid_text} color usage")
    negative_prompt = ", ".join(negative_parts)

    concept = {
        "success": True,
        "concept_generation_status": "fallback_used",
        "project_type": user_data.get("project_type", "not specified"),
        "space_type": user_data.get("space_type") or user_data.get("business_type") or "not specified",
        "concept_summary": (
            "Gemini text concept was temporarily unavailable, so Hendsetna generated "
            "the image prompt directly from your design inputs."
        ),
        "design_brief": (
            "Fallback concept generated from user inputs."
            + (f" The design must include the user's selected colors: {color_text}." if preferred_colors else "")
        ),
        "style_direction": style,
        "mood": mood,
        "color_palette": [
            {
                "name": color,
                "hex": _simple_color_hex(color),
                "usage": "Mandatory user-selected color for the core palette or tasteful accent.",
            }
            for color in preferred_colors
        ],
        "materials": [
            {"name": material, "usage": "User-selected material to incorporate in the design."}
            for material in materials
        ],
        "furniture_suggestions": [
            f"Include {item} as requested by the user." for item in furniture
        ],
        "lighting_suggestions": [
            f"Use {item} as part of the lighting setup." for item in lighting
        ],
        "layout_suggestions": [],
        "image_generation_prompt": " ".join(part for part in prompt_parts if part),
        "negative_prompt": negative_prompt,
    }
    concept["preferred_colors"] = preferred_colors
    concept["colors_to_avoid"] = colors_to_avoid

    if gemini_error:
        concept["gemini_error_details"] = str(gemini_error)

    return _enforce_design_constraints(concept, user_data)


def _normalize_response(data, user_data):
    if not isinstance(data, dict):
        raise ValueError("Gemini response was not a JSON object.")

    data["success"] = True
    data.setdefault("project_type", user_data.get("project_type", "not specified"))
    data.setdefault(
        "space_type",
        user_data.get("space_type") or user_data.get("business_type") or "not specified",
    )
    data.setdefault("design_brief", "")
    data.setdefault("concept_summary", "")
    data.setdefault("style_direction", "")
    data.setdefault("mood", "")
    data.setdefault("color_palette", [])
    data.setdefault("materials", [])
    data["furniture_suggestions"] = _normalize_list(data.get("furniture_suggestions"))
    data["lighting_suggestions"] = _normalize_list(data.get("lighting_suggestions"))
    data["layout_suggestions"] = _normalize_list(data.get("layout_suggestions"))
    data.setdefault("image_generation_prompt", "")
    data.setdefault("negative_prompt", build_negative_prompt())
    data.pop("optional_notes", None)
    return _enforce_design_constraints(data, user_data)


def _build_prompt(user_data):
    schema = required_response_schema()
    negative_prompt = build_negative_prompt()
    return f"""
You are Hendsetna, a professional AI interior design assistant for interior designers, decor engineers, and architects.

Your job is not to replace the designer. Your job is to organize the client's requirements into a realistic, practical, professional interior design concept that a designer can develop further.

Rules:
- Return valid JSON only. No markdown, no commentary, no text outside the JSON object.
- Follow this exact response shape: {json.dumps(schema, ensure_ascii=False)}
- Treat missing, empty, null, or unavailable inputs as "not specified" internally. Do not write "undefined".
- Uploaded images, logos, room photos, moodboards, and references are optional. If no upload information is present, continue normally.
- Respect budget, dimensions, area, ceiling height, users, project type, business type, mood, style, colors, materials, lighting, furniture, and notes when provided.
- User-provided colors are mandatory design constraints. You must include the preferred colors in the color_palette, design_brief, and image_generation_prompt. You must avoid any colors listed in colorsToAvoid. Do not replace the user's colors with unrelated colors.
- Every user-provided field is a design constraint. You must not ignore preferredColors, colorsToAvoid, selected materials, furniture requirements, lighting choices, style, mood, or space type. The image_generation_prompt must clearly reflect these constraints.
- Keep the concept realistic: usable circulation, correct scale, practical furniture, believable lighting, and coherent materials.
- If the client mentions a football club, brand, TV series, person, or any personal inspiration, integrate it subtly and professionally. Do not fill the room with logos. Use colors, small decor, framed art, accent objects, or palette inspiration.
- Avoid childish literal themes unless the user explicitly asked for a themed room.
- color_palette must contain 4 to 6 colors with practical hex values and usage notes.
- materials must contain 4 to 7 material suggestions with usage notes.
- image_generation_prompt is the most important field. Make it a highly detailed, single paragraph in English, ready for an image model.
- Start image_generation_prompt with "Photorealistic interior design render of a...". Include style, mood, colors, materials, furniture, lighting, and other key details. Mention colors to avoid. End with quality keywords like "high-end architectural visualization, wide-angle interior photography, realistic proportions, clean professional styling, no people unless requested."
- image_generation_prompt must not replace selected colors with random colors. If a user color is strong, use it as a controlled accent but still include it.
- Before returning JSON, verify that the image_generation_prompt includes the user's preferred colors, materials, furniture requirements, lighting setup, style, mood, and space type.
- negative_prompt should include this baseline and may add relevant constraints: {negative_prompt}

User project data:
{json.dumps(user_data, ensure_ascii=False, indent=2)}
""".strip()


def generate_design_concept(user_data):
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)
    prompt = _build_prompt(user_data)
    model_name = os.getenv("GEMINI_TEXT_MODEL", DEFAULT_TEXT_MODEL_NAME)
    print(f"Using Gemini text model: {model_name}")

    last_error = None
    for attempt_index, delay in enumerate(RETRY_DELAYS):
        if delay:
            time.sleep(delay)

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json",
                ),
            )
            break
        except Exception as exc:
            last_error = exc
            is_last_attempt = attempt_index == len(RETRY_DELAYS) - 1
            if not _is_temporary_gemini_error(exc) or is_last_attempt:
                if _is_temporary_gemini_error(exc):
                    return _gemini_unavailable_error(exc)
                raise
    else:
        return _gemini_unavailable_error(last_error)

    try:
        parsed = _json_from_text(getattr(response, "text", ""))
        return _normalize_response(parsed, user_data)
    except Exception as exc:
        return _gemini_invalid_json_error(exc)
