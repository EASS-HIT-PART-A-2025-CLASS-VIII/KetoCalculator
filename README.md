🥑 Keto Calculator

A full-stack Keto nutrition calculator that estimates calories, macros, and weight change projections based on user inputs.

Built as a learning project with:

Modern Python backend (FastAPI, uv)

Scientific formulas

Dockerized API

React + Vite frontend

Clean architecture and tests

⚠️ This project is for educational purposes only.
Results are estimates and not medical advice.

✨ Features (current)

Metric & imperial input support

BMI, BMR, TDEE calculations

Approximate body fat percentage & FFMI

Keto macros (protein, fat, net carbs)

Goal-based calorie adjustment:

Lose: −20%

Maintain: 0%

Gain: +20%

Weekly weight forecast chart

Clean UI with real-time API calls

🧠 Scientific basis (high level)

Formulas are based on commonly accepted models, including:

BMI – WHO definition

BMR – Mifflin–St Jeor equation

TDEE – activity multipliers

Weight change – ~7700 kcal per kg

Body fat % (estimate) – BMI-based approximation

FFMI – fat-free mass normalized by height

Detailed references will be added in a future update.

🏗️ Project structure
KetoCalculator/
├── backend/
│   ├── app/
│   │   ├── formulas/        # All calculation logic
│   │   ├── units.py         # Metric / imperial normalization
│   │   ├── calc.py          # Main calculation orchestrator
│   │   └── main.py          # FastAPI entry point
│   ├── tests/               # Pytest test suite
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── README.md
│
├── frontend/
│   ├── src/                 # React components
│   ├── vite.config.js       # Dev proxy to backend
│   ├── package.json
│   └── README.md
│
├── docker-compose.yml
└── README.md

🚀 Running locally (recommended for development)
1️⃣ Backend (with uv)

Requirements

Python 3.12

uv installed

cd backend
uv sync
uv run uvicorn app.main:app --reload


Backend will be available at:

http://localhost:8000

Swagger UI: http://localhost:8000/docs

2️⃣ Frontend (Vite + React)

Requirements

Node.js (LTS recommended)

npm

cd frontend
npm install
npm run dev -- --host


Frontend will be available at:

http://localhost:5173

The frontend automatically proxies API calls to the backend.

🐳 Running with Docker (backend)
Build and run API
docker build -t keto-api ./backend
docker run --rm -p 8000:8000 keto-api


Or with Docker Compose (recommended):

docker compose up --build

🔐 Environment variables

Some features (planned) require API keys.

Create a local .env file (not committed):

GOOGLE_API_KEY=your_key_here


Docker Compose will automatically load it.

🧪 Tests & code quality

From backend/:

uv run pytest
uv run ruff format .
uv run ruff check .


All calculation logic is unit-tested.

🛣️ Roadmap (planned)

LLM-generated keto meal plans

Scientific references section

Metric ↔ imperial output toggle

Mobile-responsive UI

Cloud deployment (AWS free tier)

📌 Disclaimer

This project provides estimates only and is not a substitute for professional medical or nutritional advice.

👤 Author

Built as part of an academic learning project using modern backend & frontend tooling.