# Opportunity Radar 🎯
### ET AI Hackathon 2026 — PS 6: AI for the Indian Investor

> Not a summarizer. A signal-finder.
> This project demonstrates a production-style multi-agent AI system for real-time investor decision intelligence.

An AI agent system that continuously monitors NSE/BSE corporate filings, insider trades, bulk/block deals, quarterly results, and management commentary — surfacing missed investment opportunities as actionable, plain-English signals for retail investors.

---

## Demo Video
[Watch Demo](https://drive.google.com/file/d/11xR9kQ3LRwYA_r5LI9Ou83EqeuUQUhoB/view?usp=drive_link)

## Presentation
[View PPT](https://drive.google.com/file/d/1A50Ik5X4zSRbc9VZsdrJ0KQ5ECClgJAd/view?usp=drive_link)

## 👥 Team : FutureMinds
- Mohit : Backend Development & System Integration
- Prachi Singh : AI Systems & User Experience Design

---

## 📌 Problem
India has 14 crore+ demat accounts. Most retail investors react to tips, miss filings, and can't read signals buried in exchange data. ET Markets has the data. We built the intelligence layer.

---

## 💡 Solution
Opportunity Radar is a multi-agent AI system with 5 specialized agents:
- **FilingWatcher** — monitors BSE/NSE exchange filings in real time
- **InsiderTracker** — detects insider trade clusters before price moves
- **SentimentAnalyser** — reads management commentary for tone shifts
- **SignalRanker** — scores and ranks signals by actionability
- **AlertDispatcher** — delivers plain-English alerts to the dashboard

---

## 🧠 Key Innovation
- Multi-agent architecture instead of a single AI model  
- Real-time monitoring of filings + insider trades  
- Intelligent signal ranking for decision-making  
- Plain-English alerts for non-expert users  

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

## 📊 Impact
- Helps retail investors detect opportunities early  
- Reduces dependency on tips and speculation  
- Converts complex financial data into simple insights  
- Scalable for millions of Indian investors  

> If adopted by 1 lakh users, Opportunity Radar can help prevent crores in uninformed investment losses every month.

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


## License
MIT
