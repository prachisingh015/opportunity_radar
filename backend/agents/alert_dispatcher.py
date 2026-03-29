"""
AlertDispatcher Agent
Formats ranked signals into clean, plain-English alerts
and pushes them to the WebSocket for live dashboard updates.
"""

from openai import AsyncOpenAI
import json
import os
from datetime import datetime

client = AsyncOpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ.get("GITHUB_TOKEN"),
)

MODEL = "gpt-4o"

SYSTEM_PROMPT = """You are AlertDispatcher, the final voice of Opportunity Radar.
Your job is to write CRISP, PLAIN-ENGLISH alerts that a busy retail investor can read in 10 seconds.
No jargon. No "it is worth noting". No passive voice.
Format: Hook → What happened → Why it matters → What to watch.
Max 3 sentences per alert.
Respond in JSON:
{
  "alerts": [
    {
      "id": "unique_id",
      "symbol": "STOCK",
      "headline": "under 10 words, punchy",
      "body": "3 sentences max, plain English",
      "tag": "INSIDER BUY | EARNINGS BEAT | MANAGEMENT UPGRADE | DIVIDEND | FILING ALERT",
      "direction": "bullish | bearish | neutral",
      "score": 0-100,
      "urgency": "today | this_week | this_month",
      "timestamp": "ISO timestamp"
    }
  ]
}
"""


async def alert_dispatcher_agent(state: dict) -> dict:
    ranked_signals = state.get("ranked_signals", [])
    symbol = state["stock_symbol"]

    if not ranked_signals:
        return {**state, "alerts": []}

    # Only dispatch top 5 signals
    top_signals = ranked_signals[:5]
    signals_text = json.dumps(top_signals, indent=2)

    response = await client.chat.completions.create(
        model=MODEL,
        max_tokens=1500,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Write alerts for top signals of {symbol}:\n{signals_text}\nCurrent time: {datetime.now().isoformat()}",
            },
        ],
        response_format={"type": "json_object"},
    )

    try:
        result = json.loads(response.choices[0].message.content)
        alerts = result.get("alerts", [])
        for alert in alerts:
            alert["symbol"] = symbol
    except Exception:
        alerts = []

    return {**state, "alerts": alerts}
