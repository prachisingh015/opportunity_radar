"""
FilingWatcher Agent
Fetches corporate filings from BSE/NSE and identifies anomalies:
- Surprise quarterly results
- Dividend announcements
- Board meeting notices
- Regulatory filings
"""

from openai import AsyncOpenAI
import httpx
import os

client = AsyncOpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ.get("GITHUB_TOKEN"),
)

MODEL = "gpt-4o"

NSE_FILINGS_URL = "https://www.nseindia.com/api/corp-info"
BSE_FILINGS_URL = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"

SYSTEM_PROMPT = """You are FilingWatcher, a financial analyst AI specializing in Indian stock market filings.
Your job is to analyze corporate filings and identify SIGNALS — not summaries.
A signal is something actionable: a surprise result, unusual disclosure, positive/negative catalyst.
Always respond in JSON with this structure:
{
  "signals": [
    {
      "type": "filing_surprise | dividend | board_meeting | regulatory",
      "title": "short plain-English title",
      "description": "1-2 sentence plain-English explanation of WHY this matters",
      "strength": "high | medium | low",
      "direction": "bullish | bearish | neutral"
    }
  ]
}
"""


async def fetch_filings(symbol: str) -> list[dict]:
    """Fetch filings from NSE. Falls back to mock data if API unavailable."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        }
        async with httpx.AsyncClient(timeout=10) as client_http:
            resp = await client_http.get(
                f"{NSE_FILINGS_URL}?symbol={symbol}&corpType=announcements",
                headers=headers,
            )
            if resp.status_code == 200:
                return resp.json().get("announcements", [])[:10]
    except Exception:
        pass

    # Mock fallback for demo/hackathon
    return [
        {
            "subject": f"{symbol} Q4 Results - PAT up 34% YoY, beats estimates by 12%",
            "date": "2026-03-20",
            "category": "Results",
        },
        {
            "subject": f"{symbol} announces ₹8/share dividend, record date April 15",
            "date": "2026-03-18",
            "category": "Dividend",
        },
        {
            "subject": f"Board meeting on April 2 to consider buyback proposal",
            "date": "2026-03-15",
            "category": "Board Meeting",
        },
    ]


async def filing_watcher_agent(state: dict) -> dict:
    symbol = state["stock_symbol"]
    filings = await fetch_filings(symbol)

    if not filings:
        return {**state, "raw_filings": [], "raw_signals": []}

    filings_text = "\n".join(
        [f"- [{f.get('date','')}] {f.get('subject','')}" for f in filings]
    )

    response = await client.chat.completions.create(
        model=MODEL,
        max_tokens=1000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Analyse these filings for {symbol} and find signals:\n{filings_text}",
            },
        ],
        response_format={"type": "json_object"},
    )

    import json
    try:
        result = json.loads(response.choices[0].message.content)
        signals = result.get("signals", [])
    except Exception:
        signals = []

    return {
        **state,
        "raw_filings": filings,
        "raw_signals": state.get("raw_signals", []) + signals,
    }
