"""
SignalRanker Agent
Takes all raw signals from other agents and ranks them
by actionability, strength, and confluence.
Confluence = multiple agents agree = stronger signal.
"""

from openai import AsyncOpenAI
import os

client = AsyncOpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ.get("GITHUB_TOKEN"),
)

MODEL = "gpt-4o"

SYSTEM_PROMPT = """You are SignalRanker, an expert at prioritising investment signals for retail investors.
Given a list of signals from multiple sources, rank them by:
1. Actionability — can a retail investor act on this today?
2. Strength — how significant is this signal historically?
3. Confluence — do multiple signal types agree?
4. Time sensitivity — is this time-bound?

Assign a score 1-100. Top signals should be genuinely rare and high-conviction.
Respond in JSON:
{
  "ranked_signals": [
    {
      "rank": 1,
      "score": 92,
      "type": "original type",
      "title": "title",
      "description": "description",
      "direction": "bullish | bearish | neutral",
      "confluence": true/false,
      "action": "plain-English action a retail investor can take",
      "urgency": "today | this_week | this_month"
    }
  ]
}
"""


async def signal_ranker_agent(state: dict) -> dict:
    raw_signals = state.get("raw_signals", [])

    if not raw_signals:
        return {**state, "ranked_signals": []}

    import json
    signals_text = json.dumps(raw_signals, indent=2)

    response = await client.chat.completions.create(
        model=MODEL,
        max_tokens=1500,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Rank these signals for {state['stock_symbol']}:\n{signals_text}",
            },
        ],
        response_format={"type": "json_object"},
    )

    try:
        result = json.loads(response.choices[0].message.content)
        ranked = result.get("ranked_signals", [])
    except Exception:
        ranked = []

    return {**state, "ranked_signals": ranked}
