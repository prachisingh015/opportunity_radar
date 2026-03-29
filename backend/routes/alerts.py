from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

# In production this comes from DB. For demo/hackathon, seeded mock alerts.
MOCK_ALERTS = [
    {
        "id": "a1",
        "symbol": "BAJFINANCE",
        "headline": "CEO buys ₹4.2Cr in open market",
        "body": "MD & CEO purchased 50,000 shares worth ₹4.2 crore — third consecutive insider buy this month. Promoter group added another 2L shares simultaneously. When insiders cluster-buy before results, it's worth paying attention.",
        "tag": "INSIDER BUY",
        "direction": "bullish",
        "score": 94,
        "urgency": "today",
        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
    },
    {
        "id": "a2",
        "symbol": "TCS",
        "headline": "PAT beats estimates by 12%, margin at 5-year high",
        "body": "TCS Q4 PAT at ₹12,400Cr, 12% above consensus. Operating margin hit 26.2% — highest since FY21. Management guided for double-digit revenue growth in FY27, shifting tone from cautious to confident.",
        "tag": "EARNINGS BEAT",
        "direction": "bullish",
        "score": 89,
        "urgency": "today",
        "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
    },
    {
        "id": "a3",
        "symbol": "RELIANCE",
        "headline": "Board approves ₹8/share dividend + buyback",
        "body": "Reliance declared ₹8/share dividend (record date April 15) alongside a ₹10,000Cr buyback at ₹1,560/share — 8% premium to CMP. This signals strong cash position and promoter confidence at current levels.",
        "tag": "DIVIDEND",
        "direction": "bullish",
        "score": 82,
        "urgency": "this_week",
        "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(),
    },
    {
        "id": "a4",
        "symbol": "INFY",
        "headline": "Management tone shifts from cautious to confident",
        "body": "Infosys Q4 call language changed significantly — 'headwinds' replaced by 'acceleration', capex guidance doubled to ₹3,200Cr. Order book at all-time high of $5.8B. Tone shifts like this historically precede 15-25% re-rating.",
        "tag": "MANAGEMENT UPGRADE",
        "direction": "bullish",
        "score": 78,
        "urgency": "this_week",
        "timestamp": (datetime.now() - timedelta(hours=8)).isoformat(),
    },
    {
        "id": "a5",
        "symbol": "ADANIENT",
        "headline": "Bulk deal: FII exits 1.2% stake at discount",
        "body": "A major FII offloaded 1.2% stake (₹1,800Cr) in a single bulk deal at 3% discount to previous close. While FII exits aren't always bearish, the discount signals urgency. Watch for further selling pressure.",
        "tag": "FILING ALERT",
        "direction": "bearish",
        "score": 71,
        "urgency": "today",
        "timestamp": (datetime.now() - timedelta(hours=12)).isoformat(),
    },
]


@router.get("/feed")
async def get_alert_feed(limit: int = 20):
    """Get latest signal alerts feed."""
    return {
        "alerts": MOCK_ALERTS[:limit],
        "total": len(MOCK_ALERTS),
        "last_updated": datetime.now().isoformat(),
    }


@router.get("/stats")
async def get_alert_stats():
    """Get alert statistics for dashboard."""
    return {
        "total_today": 12,
        "bullish": 8,
        "bearish": 3,
        "neutral": 1,
        "high_conviction": 4,
        "stocks_scanned": 1847,
        "last_scan": datetime.now().isoformat(),
    }
