# Hendsetna | هندستنا

> **AI-Powered Interior Design Assistant for Creative Professionals**

Hendsetna is a full-stack web application that helps interior designers, decor engineers, and architects generate a complete, professional design concept from client requirements. It uses Google Gemini to produce a structured design brief, color palette, material suggestions, furniture direction, lighting plan, and an AI-generated interior image — all in one click.

---

## Features

- 🏠 **4 Project Types** — Residential, Commercial, Administrative, Hospitality/Tourism
- 🎨 **Full Design Concept** — Design brief, style direction, mood, color palette, materials, furniture, and lighting suggestions
- 🖼️ **AI Image Generation** — Produces a photorealistic interior render via Pollinations (base64 delivered, no CORS issues)
- 🔁 **Automatic Fallback** — If Gemini is unavailable or returns malformed JSON, the system generates the concept and image prompt entirely from the user's inputs with zero downtime
- 🌍 **Bilingual UI** — English and Arabic, fully translatable via i18n system
- 📋 **Copy Prompt** — One-click export of the image generation prompt
- 📱 **Responsive Design** — Works on desktop, tablet, and mobile
- ☁️ **Vercel-ready** — Backend runs as a serverless Python function; frontend served as static files

---

## Project Structure

```
Handastna/
├── backend/                     # Flask API (Python)
│   ├── app.py                   # Flask application, API routes
│   ├── gemini_service.py        # Gemini API integration, prompt building, concept normalization
│   ├── image_prompt_service.py  # Pollinations image generation, prompt sanitization
│   ├── index.py                 # Vercel serverless entry point
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # API keys (not committed)
│   ├── test_app_fallback.py     # Tests for fallback flow in app.py
│   └── test_image_prompt_service.py  # Tests for image prompt service
│
├── frontend/                    # Static SPA (HTML/CSS/JS)
│   ├── index.html               # Main single-page application
│   ├── style.css                # All styles
│   ├── script.js                # Application logic, i18n, API calls
│   └── assets/
│       └── images/              # Static image assets
│
├── docs/                        # Project documentation
│   ├── project_idea.txt         # Original project specification
│   └── user_flow.txt            # User flow description
│
├── prompts/                     # Prompt drafts (work in progress)
│
├── __init__.py                  # Root package init (required for Vercel imports)
├── index.py                     # Root Vercel entry point
├── vercel.json                  # Vercel deployment configuration
├── .gitignore
├── .vercelignore
└── README.md
```

---

## Technologies Used

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML5, CSS3, JavaScript (ES2020+) |
| Typography | Google Fonts — Playfair Display, DM Sans, Noto Naskh Arabic |
| Backend | Python 3, Flask, Flask-CORS |
| AI Text | Google Gemini (`gemini-2.5-flash`) via `google-genai` SDK |
| AI Image | Pollinations.ai (free, no API key needed) |
| Deployment | Vercel (serverless Python + static files) |
| Environment | `python-dotenv` for local env management |

---

## Installation

### Prerequisites

- Python 3.10 or higher
- A Google Gemini API key ([get one here](https://aistudio.google.com/))

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/hendsetna.git
cd hendsetna
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the `backend/` directory:

```
backend/.env
```

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_TEXT_MODEL=gemini-2.5-flash
IMAGEN_MODEL=imagen-4.0-generate-001
```

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Your Google AI Studio API key |
| `GEMINI_TEXT_MODEL` | No | Gemini model name (default: `gemini-2.5-flash`) |
| `IMAGEN_MODEL` | No | Reserved for future Imagen integration |

> **Never commit `backend/.env` to version control.** It is already listed in `.gitignore`.

---

## Running the Backend

```bash
# From the project root, with venv active
python backend/app.py
```

The Flask server starts at **http://127.0.0.1:5000**

### Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/generate-design` | Generate a full design concept |

### Example Request

```bash
curl -X POST http://127.0.0.1:5000/api/generate-design \
  -H "Content-Type: application/json" \
  -d '{
    "projectType": "residential",
    "projectName": "My Bedroom",
    "spaceType": "Bedroom",
    "interiorStyle": "Modern Luxury",
    "preferredColors": "blue, white",
    "mood": "Calm"
  }'
```

---

## Running the Frontend

The frontend is a plain HTML/CSS/JS SPA — no build step required.

### Option A — Open directly in browser

```bash
# Windows
start frontend/index.html

# macOS
open frontend/index.html
```

> Make sure the backend is running first so API calls succeed.

### Option B — Serve with a local static server

```bash
cd frontend
python -m http.server 8080
# Open http://localhost:8080
```

The frontend auto-detects whether it's running locally (`127.0.0.1` / `localhost`) and points API calls to `http://127.0.0.1:5000`. In production (Vercel), it uses relative API paths automatically.

---

## Project Workflow

```
User fills form
    |
    v
Frontend (script.js) collects form data
    |
    v
POST /api/generate-design
    |
    v
sanitize_payload() -> normalize_user_payload()
    |
    v
generate_design_concept()  <-- Gemini API
    |
    +-- Success --> _normalize_response() --> concept dict
    |
    +-- Failure (503/429/invalid JSON)
          |
          v
    build_fallback_design_concept()  <-- user inputs only
          |
          v
generate_design_image()  <-- Pollinations API
    |
    v
Return JSON concept + base64 image
    |
    v
Frontend renders results page
```

---

## Running the Tests

```bash
# From the project root, with venv active
python -m unittest discover -s backend -p "test_*.py" -v
```

Expected output: **8 tests, 0 failures**

---

## Deploying to Vercel

1. Push the repository to GitHub
2. Import the repo in [Vercel](https://vercel.com/)
3. Add `GEMINI_API_KEY` (and optionally `GEMINI_TEXT_MODEL`) as **Environment Variables** in the Vercel project settings
4. Deploy — Vercel will detect `vercel.json` and route API calls to the serverless Python backend automatically

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---|---|---|
| `GEMINI_API_KEY is not configured` | Missing `.env` in `backend/` | Create `backend/.env` with your key |
| `ModuleNotFoundError: google.genai` | Wrong package installed | Run `pip install google-genai>=1.73.1` (not `google-generativeai`) |
| `502` from `/api/generate-design` | Gemini API error or timeout | Check your API key quota; fallback should still return a result |
| Frontend shows "check the backend" | Backend not running | Run `python backend/app.py` first |
| Images not loading | Pollinations rate limit or timeout | Retry; Pollinations is a free service with occasional delays |
| Arabic text garbled in image prompt | Non-ASCII in prompt | Handled automatically by `_ascii_only()` and `_translate_arabic_design_terms()` |

---

## Future Improvements

- [ ] **Native image upload and analysis** — Pass uploaded room photos/logos to Gemini Vision for context-aware concepts
- [ ] **Google Imagen integration** — Replace Pollinations with Imagen for higher-quality renders
- [ ] **PDF export** — Export the full design concept as a branded PDF for clients
- [ ] **Saved projects** — Store and revisit past design concepts (requires auth layer)
- [ ] **Designer dashboard** — Multi-project management with comparison view
- [ ] **Shareable links** — Generate shareable concept URLs for client review

---

*Hendsetna — Designed to empower creative professionals, not replace them.*
