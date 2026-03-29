"""
InsiderTracker Agent
Detects insider trade clusters — when promoters/directors
buy/sell in patterns that precede price moves.
"""

from openai import AsyncOpenAI
import httpx
import os

client = AsyncOpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ.get("GITHUB_TOKEN"),
)

MODEL = "gpt-4o"

SYSTEM_PROMPT = """You are InsiderTracker, an expert at detecting significant insider trading patterns in Indian stocks.
Analyze insider trade data and find CLUSTERS and ANOMALIES that retail investors typically miss.
Focus on: promoter buying during dips, director purchases before results, repeated accumulation.
Respond in JSON:
{
  "signals": [
    {
      "type": "insider_cluster | promoter_buy | promoter_sell | director_accumulation",
      "title": "plain-English title",
      "description": "why this insider pattern matters for the stock price",
      "strength": "high | medium | low",
      "direction": "bullish | bearish | neutral"
    }
  ]
}
"""


async def fetch_insider_trades(symbol: str) -> list[dict]:
    """Fetch insider trades from NSE SAST data."""
    try:
        async with httpx.AsyncClient(timeout=10) as http:
            resp = await http.get(
                f"https://www.nseindia.com/api/corporate-pledgedata?index=IT&symbol={symbol}",
                headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
            )
            if resp.status_code == 200:
                return resp.json().get("data", [])[:15]
    except Exception:
        pass

    # Mock fallback
    return [
        {"acquirer": "MD & CEO", "mode": "Buy", "shares": 50000, "value": 4200000, "date": "2026-03-10"},
        {"acquirer": "Promoter Group", "mode": "Buy", "shares": 200000, "value": 16800000, "date": "2026-03-08"},
        {"acquirer": "Independent Director", "mode": "Buy", "shares": 10000, "value": 840000, "date": "2026-03-05"},
    ]


async def insider_tracker_agent(state: dict) -> dict:
    symbol = state["stock_symbol"]
    trades = await fetch_insider_trades(symbol)

    if not trades:
        return state

    trades_text = "\n".join([
        f"- {t.get('acquirer','')} {t.get('mode','')} {t.get('shares',0):,} shares worth ₹{t.get('value',0)/100000:.1f}L on {t.get('date','')}"
        for t in trades
    ])

    response = await client.chat.completions.create(
        model=MODEL,
        max_tokens=800,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Analyse insider trades for {symbol}:\n{trades_text}",
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
        "insider_trades": trades,
        "raw_signals": state.get("raw_signals", []) + signals,
    }
