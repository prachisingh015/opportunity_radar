# Opportunity Radar 🎯
### ET AI Hackathon 2026 — PS 6: AI for the Indian Investor

> Not a summarizer. A signal-finder.

An AI agent system that continuously monitors NSE/BSE corporate filings, insider trades, bulk/block deals, quarterly results, and management commentary — surfacing missed investment opportunities as actionable, plain-English signals for retail investors.

---

## Team
- Member 1: [Your Name]
- Member 2: [Your Name]

---

## Problem
India has 14 crore+ demat accounts. Most retail investors react to tips, miss filings, and can't read signals buried in exchange data. ET Markets has the data. We built the intelligence layer.

## Solution
Opportunity Radar is a multi-agent AI system with 5 specialized agents:
- **FilingWatcher** — monitors BSE/NSE exchange filings in real time
- **InsiderTracker** — detects insider trade clusters before price moves
- **SentimentAnalyser** — reads management commentary for tone shifts
- **SignalRanker** — scores and ranks signals by actionability
- **AlertDispatcher** — delivers plain-English alerts to the dashboard

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + TailwindCSS |
| Backend | FastAPI (Python 3.11) |
| AI/Agents | LangGraph + Claude claude-sonnet-4-20250514 API |
| Data | NSE India API, BSE API, yfinance, BeautifulSoup |
| Database | PostgreSQL + Redis (cache) |
| Queue | Celery + Redis |
| Deployment | Docker + Docker Compose |

---

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Anthropic API Key

### 1. Clone & Environment Setup
```bash
git clone https://github.com/your-username/opportunity-radar.git
cd opportunity-radar
cp .env.example .env
# Fill in your API keys in .env
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Full Stack via Docker
```bash
docker-compose up --build
```

App runs at: http://localhost:5173
API runs at: http://localhost:8000
API Docs at: http://localhost:8000/docs

---

## Project Structure
```
opportunity-radar/
├── frontend/          # React + Vite UI
├── backend/           # FastAPI + LangGraph agents
├── docs/              # Architecture document
├── scripts/           # DB seed & utility scripts
├── docker-compose.yml
└── README.md
```

---

## Agent Architecture
See `docs/architecture.md` for full diagram and description.

---

## Impact Model
See `docs/impact_model.md` for quantified business impact estimates.

---

## Demo
[Link to 3-minute pitch video]

---

## License
MIT
