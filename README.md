<div align="center">

# Hendsetna | هندستنا

### AI Interior Design Assistant for Creative Professionals

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=flat&logo=google&logoColor=white)](https://aistudio.google.com)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat)]()

</div>

---

Hendsetna is a full-stack web application that helps **interior designers, decor engineers, and architects** turn scattered client requirements into a complete, structured design concept — in one click.

It collects project details through a guided bilingual form (English / Arabic), sends them to **Google Gemini** to generate a professional design brief, color palette, material suggestions, furniture plan, and lighting direction, then calls **Pollinations.ai** to render a photorealistic interior image — all returned as a single JSON response to the frontend.

> Hendsetna does not replace the designer. It organises client requirements and creates an initial visual concept the designer can develop further.

---

## Features

| Feature | Description |
|---|---|
| 🏠 **4 Project Types** | Residential · Commercial · Administrative · Hospitality/Tourism |
| 🧠 **Gemini-powered Concepts** | Design brief, style direction, mood, color palette, materials, furniture, lighting |
| 🖼️ **AI Image Generation** | Photorealistic render via Pollinations.ai — delivered as base64, no CORS issues |
| 🔁 **Automatic Fallback** | If Gemini is unavailable or returns invalid JSON, a full concept is still generated directly from the user's inputs — zero downtime |
| 🌍 **Bilingual UI** | Full English ↔ Arabic toggle via a built-in i18n system |
| 📋 **Copy Prompt** | One-click export of the image generation prompt for use in other tools |
| 📱 **Responsive Design** | Works on desktop, tablet, and mobile |
| ☁️ **Vercel-ready** | Backend runs as a serverless Python function; frontend served as static files |

---

## Screenshots

> _Screenshots can be added here once the app is deployed._

| Home | Design Form | Results |
|---|---|---|
| _(placeholder)_ | _(placeholder)_ | _(placeholder)_ |

---

## Project Structure

```
Handastna/
│
├── backend/                          # Python Flask API
│   ├── app.py                        # Flask app — API routes, request validation
│   ├── gemini_service.py             # Gemini integration, prompt building, response normalization
│   ├── image_prompt_service.py       # Pollinations image generation, Arabic translation, prompt sanitization
│   ├── index.py                      # Vercel serverless entry point (imports app from backend)
│   ├── requirements.txt              # Python dependencies (pinned)
│   ├── .env                          # API keys — NOT committed to version control
│   ├── test_app_fallback.py          # Unit tests: fallback flow and endpoint behavior
│   └── test_image_prompt_service.py  # Unit tests: Pollinations prompt builder
│
├── frontend/                         # Vanilla HTML/CSS/JS single-page app
│   ├── index.html                    # Full SPA markup (navbar, forms, results)
│   ├── style.css                     # All styles
│   ├── script.js                     # App logic — i18n, form collection, API calls, result rendering
│   └── assets/
│       └── images/                   # Static image assets
│
├── docs/                             # Project documentation
│   ├── project_idea.txt              # Original project specification
│   └── user_flow.txt                 # User flow description
│
├── prompts/                          # Prompt drafts (work in progress)
│
├── __init__.py                       # Root Python package (required for Vercel module resolution)
├── index.py                          # Root Vercel entry point — patches sys.path and imports app
├── vercel.json                       # Vercel routing configuration
├── .gitignore
├── .vercelignore
└── README.md
```

---

## Technologies

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES2020+) | Single-page application |
| **Fonts** | Google Fonts — Playfair Display, DM Sans, Noto Naskh Arabic | Typography |
| **Backend** | Python 3.10+, Flask 3.1+ | REST API |
| **CORS** | Flask-CORS | Cross-origin support for local development |
| **AI Text** | Google Gemini `gemini-2.5-flash` via `google-genai` SDK | Design concept generation |
| **AI Image** | [Pollinations.ai](https://pollinations.ai) | Free photorealistic image rendering |
| **Env Vars** | `python-dotenv` | Local environment configuration |
| **Deployment** | Vercel | Serverless Python backend + static frontend |

---

## Requirements

- **Python** 3.10 or higher
- A **Google Gemini API key** — [get one free at Google AI Studio](https://aistudio.google.com/)
- Internet access (calls Gemini API and Pollinations.ai at runtime)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/samahelmenady/hendsetna.git
cd hendsetna
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Environment Variables

Create a file named `.env` inside the `backend/` directory:

**`backend/.env`**

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_TEXT_MODEL=gemini-2.5-flash
IMAGEN_MODEL=imagen-4.0-generate-001
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | — | Your Google AI Studio API key |
| `GEMINI_TEXT_MODEL` | No | `gemini-2.5-flash` | Gemini text model to use |
| `IMAGEN_MODEL` | No | — | Reserved for future Google Imagen integration |

> ⚠️ **`backend/.env` is listed in `.gitignore` and must never be committed to version control.**

---

## Running Locally

### Start the backend

```bash
# From the project root, with venv active
python backend/app.py
```

The Flask development server starts at **`http://127.0.0.1:5000`**

To enable debug/auto-reload mode:

```bash
# Windows
set FLASK_DEBUG=1 && python backend/app.py

# macOS / Linux
FLASK_DEBUG=1 python backend/app.py
```

---

### Open the frontend

The frontend is a static SPA — no build step is required.

**Option A — Open the file directly:**

```bash
# Windows
start frontend\index.html

# macOS
open frontend/index.html
```

**Option B — Serve it with Python's built-in server (recommended):**

```bash
cd frontend
python -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

> The frontend automatically detects `localhost` / `127.0.0.1` and sends API requests to `http://127.0.0.1:5000`. In production (Vercel), it uses relative paths — no configuration needed.

---

## API Endpoints

Base URL (local): `http://127.0.0.1:5000`

---

### `GET /api/health`

Health check — confirms the backend is running.

**Response `200 OK`:**
```json
{ "status": "ok" }
```

---

### `POST /api/generate-design`

Generates a complete interior design concept from the provided project details.

**Request headers:**
```
Content-Type: application/json
```

**Request body** (camelCase keys are normalised server-side):

| Field | Type | Required | Description |
|---|---|---|---|
| `projectType` | string | ✅ | `residential`, `commercial`, `administrative`, or `hospitality` |
| `projectName` | string | ✅ | Name of the project |
| `spaceType` | string | ✅* | Space type for residential / administrative / hospitality |
| `businessType` | string | ✅* | Business type for commercial projects |
| `interiorStyle` | string | No | e.g. `Modern Luxury`, `Arabic Luxury` |
| `mood` | string | No | e.g. `Calm`, `Energetic` |
| `preferredColors` | string | No | Comma-separated preferred colors |
| `colorsToAvoid` | string | No | Comma-separated colors to avoid |
| `materials` | string / array | No | e.g. `["wood", "marble", "glass"]` |
| `furnitureRequirements` | string | No | Free-text furniture description |
| `lighting` | string | No | Lighting preferences |
| `area` | string | No | Floor area in m² |
| `ceilingHeight` | string | No | Ceiling height in metres |
| `numUsers` | string | No | Number of occupants |
| `personalInspiration` | string | No | Free-text inspiration reference |
| `brandName` | string | No | Brand name (commercial) |
| `brandColors` | string | No | Brand color palette (commercial) |

> *`spaceType` or `businessType` — at least one is required depending on project type.

**Example request:**

```bash
curl -X POST http://127.0.0.1:5000/api/generate-design \
  -H "Content-Type: application/json" \
  -d '{
    "projectType": "residential",
    "projectName": "Blue Bedroom",
    "spaceType": "Bedroom",
    "interiorStyle": "Modern Luxury",
    "mood": "Calm",
    "preferredColors": "blue, white, light wood",
    "colorsToAvoid": "red, black",
    "materials": ["wood", "fabric", "glass"],
    "furnitureRequirements": "one bed, small desk, large wardrobe",
    "lighting": "warm hidden LED, pendant lights"
  }'
```

**Success response `200 OK`:**

```json
{
  "success": true,
  "project_type": "residential",
  "space_type": "Bedroom",
  "design_brief": "A calm Modern Luxury bedroom with blue and white tones...",
  "concept_summary": "...",
  "style_direction": "Modern Luxury",
  "mood": "Calm",
  "color_palette": [
    { "name": "Deep Blue", "hex": "#2F6FDB", "usage": "Primary wall accent" },
    { "name": "White", "hex": "#FFFFFF", "usage": "Ceiling and trim" }
  ],
  "materials": [
    { "name": "Light Wood", "usage": "Flooring and furniture veneer" }
  ],
  "furniture_suggestions": ["Low-profile queen bed", "Floating desk", "Built-in wardrobe"],
  "lighting_suggestions": ["Warm hidden LED cove", "Bedside pendant lights"],
  "layout_suggestions": ["Bed centered on feature wall", "Desk near window"],
  "image_generation_prompt": "Photorealistic interior design render of a Bedroom...",
  "negative_prompt": "distorted furniture, unrealistic proportions...",
  "image_generation_status": "success",
  "image_provider": "pollinations",
  "image_url": "https://image.pollinations.ai/prompt/...",
  "image_url_prompt": "Photorealistic interior design render of a Bedroom...",
  "image_base64": "<base64-encoded-jpeg>",
  "image_mime_type": "image/jpeg",
  "preferred_colors": ["blue", "white", "light wood"],
  "colors_to_avoid": ["red", "black"]
}
```

**Validation error `400 Bad Request`:**

```json
{
  "error": "Missing required fields.",
  "details": ["project_name is required.", "space_type or business_type is required."]
}
```

**Server error `502 Bad Gateway`:**

```json
{
  "error": "Could not generate the design concept right now.",
  "details": "..."
}
```

---

## Architecture & Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                       FRONTEND (browser)                    │
│  User fills the design form (HTML/CSS/JS)                   │
│  → collectFormData()  → POST /api/generate-design           │
└────────────────────────────┬────────────────────────────────┘
                             │ JSON payload
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (Flask)                        │
│                                                             │
│  sanitize_payload()  →  normalize_user_payload()            │
│       │                                                     │
│       ▼                                                     │
│  generate_design_concept()  ──►  Google Gemini API          │
│       │                          (gemini-2.5-flash)        │
│       ├── ✅ Gemini OK  → _normalize_response()             │
│       │                                                     │
│       └── ❌ Gemini fails (503 / 429 / invalid JSON)        │
│                  │                                          │
│                  ▼                                          │
│         build_fallback_design_concept()                     │
│         (builds full concept from user inputs only)         │
│                  │                                          │
│       ┌──────────┘                                          │
│       ▼                                                     │
│  generate_design_image()  ──►  Pollinations.ai              │
│       │                    (fetches image → base64)         │
│       ▼                                                     │
│  Return merged JSON concept + image                         │
└────────────────────────────┬────────────────────────────────┘
                             │ JSON response
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                       FRONTEND (browser)                    │
│  renderDesignResult()  →  displays palette, brief,          │
│  materials, furniture, lighting, and AI image               │
└─────────────────────────────────────────────────────────────┘
```

### Key design decisions

- **Fallback system** — Gemini errors never crash the app. The backend detects `gemini_unavailable` and `gemini_invalid_json` error types and automatically reroutes to a local concept-builder that uses the raw user inputs.
- **Prompt safety** — Before sending to Pollinations, Arabic text is transliterated, non-ASCII characters are stripped, and the prompt is trimmed to ≤ 600 characters to ensure a clean, URL-safe image request.
- **Retry with back-off** — Gemini calls retry up to 3 times (`0s / 2s / 5s`) on transient errors (503, 429, timeout) before falling back.

---

## Testing

Tests use Python's built-in `unittest` module. No additional test dependencies are needed.

```bash
# From the project root, with venv active
python -m unittest discover -s backend -p "test_*.py" -v
```

**Expected output:**

```
test_endpoint_uses_fallback_when_gemini_is_unavailable ... ok
test_endpoint_uses_fallback_when_gemini_returns_invalid_json ... ok
test_fallback_concept_has_required_fields ... ok
test_fallback_concept_includes_required_user_inputs ... ok
test_generate_design_image_returns_expected_keys ... ok
test_safe_prompt_includes_avoided_colors ... ok
test_safe_prompt_includes_preferred_colors ... ok
test_safe_prompt_is_short_english_and_keeps_core_constraints ... ok

Ran 8 tests in ~4s

OK
```

### Test files

| File | What it tests |
|---|---|
| `backend/test_app_fallback.py` | Flask endpoint behavior, fallback trigger on Gemini failure, response structure |
| `backend/test_image_prompt_service.py` | Pollinations safe-prompt builder, color constraint inclusion, `generate_design_image` return contract |

---

## Deployment (Vercel)

The project is configured for [Vercel](https://vercel.com) deployment via `vercel.json`.

### Steps

1. **Push** the repository to GitHub (ensure `backend/.env` is not committed)
2. **Import** the repo in the [Vercel dashboard](https://vercel.com/new)
3. **Add environment variables** in the Vercel project settings:
   - `GEMINI_API_KEY` ← your Gemini API key
   - `GEMINI_TEXT_MODEL` ← `gemini-2.5-flash` (optional)
4. **Deploy** — Vercel auto-detects the Python runtime and routes requests

> **Note:** The `vercel.json` routes are defined for Vercel's serverless Python runtime. The backend entry point is `backend/index.py`.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `RuntimeError: GEMINI_API_KEY is not configured` | `backend/.env` missing or not loaded | Create `backend/.env` with your `GEMINI_API_KEY` |
| `ModuleNotFoundError: No module named 'google.genai'` | Wrong package installed | Run `pip install google-genai>=1.73.1` (**not** `google-generativeai`) |
| Frontend says "check the backend and try again" | Backend not running | Start the backend: `python backend/app.py` |
| `502` response from the API | Unhandled exception in backend | Check the Flask console output for the traceback |
| Image placeholder shown instead of render | Pollinations timeout or rate limit | Retry — Pollinations is a free service with occasional delays |
| Arabic text missing from the image | Non-ASCII stripped for URL safety | Expected behavior — Arabic terms are translated to English equivalents before being sent to Pollinations |
| `git push` rejected | Remote has commits not in local branch | Run `git pull --rebase origin main` then push again |

---

## Future Improvements

- [ ] **Image upload & vision analysis** — Pass uploaded room photos, logos, or moodboards to Gemini Vision for richer, context-aware concepts
- [ ] **Google Imagen integration** — Replace Pollinations with Imagen for production-quality, controllable renders
- [ ] **PDF export** — Download the full design concept as a branded, client-ready PDF
- [ ] **Project history** — Save and revisit past concepts (requires authentication layer)
- [ ] **Designer dashboard** — Multi-project management with a side-by-side comparison view
- [ ] **Shareable concept links** — Generate public URLs for client review without requiring an account

---

## License

This project is proprietary. All rights reserved.

---

## Author

**Samah El-Menady**
GitHub: [@samahelmenady](https://github.com/samahelmenady)

---

<div align="center">
<i>Hendsetna — Designed to empower creative professionals, not replace them.</i>
</div>
