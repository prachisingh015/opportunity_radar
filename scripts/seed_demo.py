"""
Seed script — populates DB with demo signals for hackathon presentation.
Run: python scripts/seed_demo.py
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from agents.orchestrator import run_radar

DEMO_STOCKS = ["RELIANCE", "TCS", "BAJFINANCE", "INFY", "TATAMOTORS"]


async def seed():
    print("🌱 Seeding demo signals...")
    for symbol in DEMO_STOCKS:
        print(f"  Scanning {symbol}...")
        try:
            result = await run_radar(symbol)
            alerts = result.get("alerts", [])
            print(f"  ✅ {symbol}: {len(alerts)} alerts generated")
        except Exception as e:
            print(f"  ❌ {symbol}: {e}")
    print("Done!")


if __name__ == "__main__":
    asyncio.run(seed())
