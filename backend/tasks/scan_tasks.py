from celery_app import celery_app
import asyncio
from agents.orchestrator import run_radar

NSE_TOP_50 = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "BAJFINANCE",
    "WIPRO", "TATAMOTORS", "ADANIENT", "SUNPHARMA", "ICICIBANK",
    "HINDUNILVR", "KOTAKBANK", "AXISBANK", "LTIM", "HCLTECH",
    "MARUTI", "ULTRACEMCO", "TITAN", "ASIANPAINT", "NTPC",
]


@celery_app.task(bind=True, max_retries=3)
def scan_single_stock(self, symbol: str):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_radar(symbol))
        loop.close()
        return {"symbol": symbol, "signals": len(result.get("ranked_signals", []))}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@celery_app.task
def scan_watchlist():
    for symbol in NSE_TOP_50:
        scan_single_stock.delay(symbol)
    return f"Queued {len(NSE_TOP_50)} stocks"


@celery_app.task
def full_market_scan():
    for symbol in NSE_TOP_50:
        scan_single_stock.delay(symbol)
    return f"Morning scan queued for {len(NSE_TOP_50)} stocks"
