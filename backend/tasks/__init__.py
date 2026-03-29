from celery_app import celery_app
import asyncio
from agents.orchestrator import run_radar

NSE_TOP_50 = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "BAJFINANCE",
    "WIPRO", "TATAMOTORS", "ADANIENT", "SUNPHARMA", "ICICIBANK",
    "HINDUNILVR", "KOTAKBANK", "AXISBANK", "LTIM", "HCLTECH",
    "MARUTI", "ULTRACEMCO", "TITAN", "ASIANPAINT", "NTPC",
    "POWERGRID", "ONGC", "COALINDIA", "JSWSTEEL", "TATASTEEL",
    "SBIN", "INDUSINDBK", "BAJAJFINSV", "NESTLEIND", "BRITANNIA",
    "DRREDDY", "CIPLA", "DIVISLAB", "APOLLOHOSP", "TATACONSUM",
    "TECHM", "GRASIM", "HINDALCO", "VEDL", "BPCL",
    "EICHERMOT", "HERO MOTOCORP", "BAJAJ-AUTO", "M&M", "SHRIRAMFIN",
    "ADANIPORTS", "ADANIGREEN", "ADANITRANS", "ZOMATO", "NYKAA",
]


@celery_app.task(bind=True, max_retries=3)
def scan_single_stock(self, symbol: str):
    """Scan a single stock — called by watchlist scan."""
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
    """Scan top 50 NSE stocks — runs every 30 min during market hours."""
    for symbol in NSE_TOP_50[:20]:  # Batch of 20 for demo
        scan_single_stock.delay(symbol)
    return f"Queued {min(20, len(NSE_TOP_50))} stocks for scanning"


@celery_app.task
def full_market_scan():
    """Full market scan at 9:15 AM IST — morning signal digest."""
    for symbol in NSE_TOP_50:
        scan_single_stock.delay(symbol)
    return f"Morning scan queued for {len(NSE_TOP_50)} stocks"
