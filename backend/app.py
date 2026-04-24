import os

from flask import Flask, jsonify, request
from flask_cors import CORS

try:
    from gemini_service import (
        build_fallback_design_concept, generate_design_concept,
        normalize_user_payload, sanitize_payload
    )
    from image_prompt_service import generate_design_image, build_negative_prompt
except ImportError:
    from .gemini_service import (
        build_fallback_design_concept, generate_design_concept,
        normalize_user_payload, sanitize_payload
    )
    from .image_prompt_service import generate_design_image, build_negative_prompt


app = Flask(__name__)
CORS(app)


PROJECT_TYPE_ALIASES = {
    "res": "residential", "com": "commercial", "adm": "administrative", "hos": "hospitality"
}


def _validate_payload(data):
    errors = []
    if not data.get("project_type"):
        errors.append("project_type is required.")
    if not data.get("project_name"):
        errors.append("project_name is required.")
    if not (data.get("space_type") or data.get("business_type")):
        errors.append("space_type or business_type is required.")

    return errors


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/generate-design")
def generate_design():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    payload = sanitize_payload(request.get_json(silent=True) or {})
    user_data = normalize_user_payload(payload)
    errors = _validate_payload(user_data)
    if errors:
        return jsonify({"error": "Missing required fields.", "details": errors}), 400

    try:
        concept = generate_design_concept(user_data)
        error_type = concept.get("error_type")

        if error_type in {"gemini_unavailable", "gemini_invalid_json"}:
            app.logger.warning(
                f"Gemini failed ({error_type}), using fallback. Details: {concept.get('details')}"
            )
            print(f"Gemini invalid/unavailable ({error_type}); using fallback prompt.")
            concept = build_fallback_design_concept(user_data, gemini_error=concept)

        image_result = generate_design_image(concept, user_data)
        concept.update(image_result)

        if not concept.get("success"):
            concept["success"] = concept.get("image_generation_status") == "success"

        return jsonify(concept)
    except Exception as exc:
        app.logger.exception("Failed to generate design concept")
        return jsonify({
            "error": "Could not generate the design concept right now.",
            "details": str(exc),
        }), 502


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=5000, debug=debug)
