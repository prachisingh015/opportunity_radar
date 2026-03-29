# Opportunity Radar — Architecture Document
### ET AI Hackathon 2026 · PS 6: AI for the Indian Investor

---

## 1. System Overview

Opportunity Radar is a multi-agent AI system that continuously monitors the Indian stock market —
scanning NSE/BSE filings, insider trades, bulk/block deals, and management commentary —
to surface missed investment opportunities as plain-English signals for retail investors.

**Core principle:** Not a summarizer. A signal-finder.

---

## 2. Agent Architecture

### Agent 1 — FilingWatcher
- **Role:** Monitors BSE/NSE exchange announcements in real time
- **Inputs:** NSE Corp Info API, BSE Announcements API
- **Detects:** Surprise quarterly results, dividend announcements, board meeting notices, regulatory filings
- **Output:** Structured filing signals with direction (bullish/bearish) and strength

### Agent 2 — InsiderTracker
- **Role:** Detects insider trade clusters that precede price moves
- **Inputs:** NSE SAST data, promoter shareholding disclosures
- **Detects:** Director/promoter buying clusters, repeated accumulation, pre-results purchases
- **Output:** Insider trade signals ranked by cluster strength

### Agent 3 — SentimentAnalyser
- **Role:** Reads management commentary for tone SHIFTS (not just sentiment)
- **Inputs:** Earnings call transcripts, press releases, annual report excerpts
- **Detects:** Guidance upgrades, capex commitments, margin improvement signals, expansion language
- **Output:** Sentiment direction, tone shift (improving/deteriorating), key commentary signals

### Agent 4 — SignalRanker
- **Role:** Aggregates signals from all 3 upstream agents and ranks by actionability
- **Inputs:** All raw signals from Agents 1–3
- **Scoring criteria:** Actionability, historical strength, confluence (multiple agents agree), time sensitivity
- **Output:** Ranked signal list with scores (1–100), urgency, and suggested action

### Agent 5 — AlertDispatcher
- **Role:** Converts ranked signals into crisp, plain-English alerts (3 sentences max)
- **Inputs:** Top-ranked signals from Agent 4
- **Output:** Formatted alerts pushed to dashboard via WebSocket

---

## 3. Communication Flow

```
User request / Celery scheduler
         │
         ▼
   Orchestrator (LangGraph StateGraph)
         │
         ├──► FilingWatcher  ──┐
         │                     │
         ├──► InsiderTracker   ├──► SignalRanker ──► AlertDispatcher ──► WebSocket
         │                     │
         └──► SentimentAnalyser┘
```

LangGraph manages the agent state (`RadarState`) through the pipeline.
Each agent receives the full state and appends its findings to `raw_signals`.
SignalRanker consumes all raw signals and produces `ranked_signals`.
AlertDispatcher formats the top 5 and pushes to the WebSocket bus.

---

## 4. Tool Integrations

| Tool / Service | Purpose |
|---|---|
| **Anthropic Claude claude-sonnet-4-20250514** | All 5 agents use Claude for analysis, signal detection, and alert generation |
| **LangGraph** | Multi-agent orchestration and state management |
| **NSE India API** | Corporate filings, announcements, insider data |
| **BSE API** | Supplementary filing data |
| **yfinance** | Real-time price quotes and OHLCV history |
| **FastAPI** | REST API + WebSocket server |
| **Celery + Redis** | Background job scheduling (market-hours scanning) |
| **PostgreSQL** | Signal storage and historical audit trail |
| **React + Vite** | Frontend dashboard |
| **lightweight-charts** | Candlestick chart rendering |

---

## 5. Error Handling & Resilience

- Each agent has a try/catch with graceful fallback to mock data (for demo/hackathon)
- LangGraph state is immutable at each step — agent failures don't corrupt pipeline state
- API failures (NSE/BSE rate limits, timeouts) fall back to cached data via Redis
- Celery retries failed scans up to 3 times with exponential backoff
- WebSocket disconnections are handled gracefully — clients reconnect automatically

---

## 6. Data Flow Diagram

```
NSE/BSE APIs ──► FilingWatcher ──────────────────────┐
                                                       │
NSE SAST Data ──► InsiderTracker ──────────────────► SignalRanker ──► AlertDispatcher ──► Dashboard
                                                       │
Earnings Calls ──► SentimentAnalyser ─────────────────┘
                                         ▲
                                   LangGraph State
                                   (RadarState)
```

---

## 7. Frontend Architecture

```
React App (Vite)
├── Layout (sidebar nav, market status, IST clock)
├── Dashboard (stat cards, signal feed, watchlist)
├── Signal Feed (filterable real-time alerts)
├── Scanner (stock search → agent pipeline → results)
└── Stock Detail (candlestick chart + scan CTA)
```

State managed via Zustand. Real-time updates via WebSocket.

---

## 8. Deployment

- Fully containerized via Docker Compose
- Services: frontend, backend, celery_worker, celery_beat, postgres, redis
- Production-ready: environment variables, CORS config, health checks
