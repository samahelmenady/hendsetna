# Hendsetna | هندستنا

Hendsetna is an AI-powered interior design assistant website that helps interior designers and decor engineers generate a complete interior design concept based on client preferences, space details, colors, materials, furniture requirements, lighting choices, and personal inspiration.

The project supports Arabic and English and generates a professional design concept with a suggested AI-generated image prompt and image preview.

---

## Project Idea

Interior designers often spend a lot of time collecting scattered client requirements and turning vague preferences into a clear design direction.

Hendsetna helps organize this process by allowing the designer to enter project details, then the system generates:

- Design brief
- Concept summary
- Style direction
- Mood description
- Color palette
- Material suggestions
- Furniture suggestions
- Lighting suggestions
- Layout suggestions
- Image generation prompt
- Suggested design image preview

---

## Main Features

- Arabic / English language support
- Project type selection:
  - Residential
  - Commercial
  - Administrative
  - Hospitality / Tourism
- Dedicated forms for different project types
- Smart lighting input section
- Optional inspiration inputs
- Gemini-powered design concept generation
- Pollinations image generation preview
- Responsive frontend interface
- Flask backend API

---

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- Gemini API
- Pollinations image generation

### Deployment
- GitHub
- Vercel

---

## Project Structure

```text
hendsetna/
│
├── backend/
│   ├── app.py
│   ├── gemini_service.py
│   ├── image_prompt_service.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── assets/
│
├── public/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── assets/
│
├── api/
│   └── index.py
│
├── docs/
├── prompts/
├── vercel.json
└── README.md

Created by Samah Elmenady.
