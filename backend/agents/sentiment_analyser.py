"""
SentimentAnalyser Agent
Reads management commentary from earnings call transcripts,
annual reports, and press releases to detect tone shifts.
"""

from openai import AsyncOpenAI
import httpx
import os

client = AsyncOpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ.get("GITHUB_TOKEN"),
)

MODEL = "gpt-4o"

SYSTEM_PROMPT = """You are SentimentAnalyser, an expert at reading between the lines of management commentary in Indian corporate communications.
Detect tone SHIFTS — not just positive/negative sentiment. A shift from cautious to confident language is more meaningful than just "positive."
Look for: guidance upgrades, capex commitment, new order wins, geographic expansion signals, margin improvement language.
Respond in JSON:
{
  "overall_tone": "bullish | cautious | bearish | mixed",
  "tone_shift": "improving | deteriorating | stable",
  "signals": [
    {
      "type": "guidance_upgrade | capex_signal | order_win | margin_commentary | expansion",
      "title": "plain-English title",
      "description": "what management said and why it matters",
      "strength": "high | medium | low",
      "direction": "bullish | bearish | neutral",
      "quote": "brief relevant excerpt"
    }
  ]
}
"""


async def fetch_management_commentary(symbol: str) -> str:
    """Fetch latest management commentary. Uses mock for hackathon."""
    # In production: scrape ET Markets earnings call transcripts,
    # or use MoneyControl/BSE press releases
    return f"""
    {symbol} Q4 FY26 Earnings Call — MD Commentary:
    "We are very confident about the trajectory going into FY27. Order book has never been stronger —
    we're sitting at 3.2x book-to-bill. Margins have structurally improved — this is not a one-quarter
    blip. We're guiding for 300-350 bps EBITDA expansion next year. On capex, we're committing ₹800 crore
    over 18 months — capacity will double by Q2 FY27. International revenue now at 28% — targeting 40%
    in 2 years. I want to be direct: the last 2 years of investment are now converting to cash flows."
    
    CFO Commentary:
    "Working capital has improved by 18 days. Cash conversion cycle is at the best level in 5 years.
    Debt has come down ₹320 crore this quarter. We are net cash positive for the first time. Dividend
    payout ratio will increase from 20% to 35% starting next year."
    """


async def sentiment_analyser_agent(state: dict) -> dict:
    symbol = state["stock_symbol"]
    commentary = await fetch_management_commentary(symbol)

    response = await client.chat.completions.create(
        model=MODEL,
        max_tokens=1000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Analyse management commentary for {symbol}:\n{commentary}",
            },
        ],
        response_format={"type": "json_object"},
    )

    import json
    try:
        result = json.loads(response.choices[0].message.content)
        signals = result.get("signals", [])
        sentiment = {
            "overall_tone": result.get("overall_tone", "mixed"),
            "tone_shift": result.get("tone_shift", "stable"),
        }
    except Exception:
        signals = []
        sentiment = {"overall_tone": "mixed", "tone_shift": "stable"}

    return {
        **state,
        "sentiment_data": sentiment,
        "raw_signals": state.get("raw_signals", []) + signals,
    }
