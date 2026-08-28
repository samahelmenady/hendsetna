<div align="center">

<img src="https://img.shields.io/badge/Hendsetna-هندستنا-1E3A5F?style=for-the-badge&labelColor=C4A07D" alt="Hendsetna">

### AI Interior Design Assistant for Creative Professionals

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://aistudio.google.com)
[![Tests](https://img.shields.io/badge/Tests-8_passing-2ea44f?style=flat-square&logo=checkmarx&logoColor=white)]()
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)]()

<br/>

> Transform client preferences into a complete interior design concept — with a generated image — in one click.

</div>

---

## What is Hendsetna?

Hendsetna collects project details through a bilingual (EN / AR) guided form, sends them to **Google Gemini** to generate a structured design concept (brief · palette · materials · furniture · lighting), then produces a **photorealistic render** via Pollinations.ai — all returned in a single API response.

If Gemini is unavailable, a **built-in fallback** generates the full concept directly from user inputs — no downtime.

---

## Features

- 🏠 **4 project types** — Residential · Commercial · Administrative · Hospitality
- 🎨 **Full design concept** — Brief, style, mood, palette, materials, furniture, lighting
- 🖼️ **AI image generation** — Photorealistic render, base64-delivered (no CORS friction)
- 🔁 **Graceful fallback** — Concept still generated when Gemini is unavailable
- 🌍 **Bilingual** — Full English ↔ Arabic toggle, no page reload
- 📋 **Copy prompt** — One-click export of the image generation prompt
- ☁️ **Vercel-ready** — Serverless Python backend + static frontend

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML · CSS · JavaScript (ES2020) |
| Backend | Python 3.10 · Flask 3.1 · Flask-CORS |
| AI Text | Google Gemini `gemini-2.5-flash` via `google-genai` |
| AI Image | [Pollinations.ai](https://pollinations.ai) — free, no key needed |
| Deployment | Vercel (serverless) |

---

## Project Structure

```
Handastna/
├── backend/
│   ├── app.py                   # API routes & request validation
│   ├── gemini_service.py        # Gemini integration + fallback logic
│   ├── image_prompt_service.py  # Pollinations prompt builder & image fetch
│   ├── index.py                 # Vercel serverless entry point
│   ├── requirements.txt
│   ├── test_app_fallback.py
│   └── test_image_prompt_service.py
├── frontend/
│   ├── index.html               # Single-page application
│   ├── style.css
│   ├── script.js                # i18n · form logic · API calls · result rendering
│   └── assets/images/
├── docs/                        # Extended documentation
│   ├── API.md                   # Full endpoint reference & examples
│   ├── ARCHITECTURE.md          # System design & data flow
│   └── TROUBLESHOOTING.md       # Common issues & fixes
├── index.py                     # Root Vercel entry point
├── vercel.json
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- A [Google Gemini API key](https://aistudio.google.com/)

### Install

```bash
git clone https://github.com/samahelmenady/Hendstna.git
cd Hendstna

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r backend/requirements.txt
```

### Configure

Create `backend/.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_TEXT_MODEL=gemini-2.5-flash
```

---

## Run Locally

**Backend** (starts at `http://127.0.0.1:5000`):

```bash
python backend/app.py
```

**Frontend** (open in browser or serve statically):

```bash
cd frontend
python -m http.server 8080
# → http://localhost:8080
```

> The frontend auto-detects `localhost` and points API calls to port 5000. No config needed.

---

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/generate-design` | Generate design concept + image |

**Quick example:**

```bash
curl -X POST http://127.0.0.1:5000/api/generate-design \
  -H "Content-Type: application/json" \
  -d '{"projectType":"residential","projectName":"My Room","spaceType":"Bedroom","interiorStyle":"Modern Luxury","preferredColors":"blue, white"}'
```

→ Full request schema, response fields, and error codes in [`docs/API.md`](docs/API.md).

---

## Tests

```bash
python -m unittest discover -s backend -p "test_*.py" -v
# Ran 8 tests — OK
```

---

## Deployment

Deployed on [Vercel](https://vercel.com). To deploy your own:

1. Push to GitHub
2. Import the repo in Vercel
3. Add `GEMINI_API_KEY` in **Project → Settings → Environment Variables**
4. Deploy

---

## Documentation

| Doc | Contents |
|---|---|
| [`docs/API.md`](docs/API.md) | Full endpoint reference, all request fields, response examples |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System design, data flow, fallback strategy |
| [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | Common errors and fixes |

---

## Author

**Samah El-Menady** · [@samahelmenady](https://github.com/samahelmenady)

---

<div align="center">
<sub>Hendsetna — Designed to empower creative professionals, not replace them.</sub>
</div>
