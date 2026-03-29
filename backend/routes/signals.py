from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from agents.orchestrator import run_radar
from typing import List, Optional

router = APIRouter()


class SignalRequest(BaseModel):
    symbol: str


class SignalResponse(BaseModel):
    symbol: str
    alerts: List[dict]
    ranked_signals: List[dict]
    sentiment: dict
    total_signals: int


@router.post("/scan", response_model=SignalResponse)
async def scan_stock(request: SignalRequest):
    """Run full Opportunity Radar scan for a stock symbol."""
    symbol = request.symbol.upper().strip()
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")

    try:
        result = await run_radar(symbol)
        return SignalResponse(
            symbol=symbol,
            alerts=result.get("alerts", []),
            ranked_signals=result.get("ranked_signals", []),
            sentiment=result.get("sentiment_data", {}),
            total_signals=len(result.get("ranked_signals", [])),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/watchlist")
async def get_watchlist_signals():
    """Get signals for default watchlist stocks."""
    watchlist = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "BAJFINANCE"]
    results = []
    for symbol in watchlist:
        try:
            result = await run_radar(symbol)
            top_alert = result.get("alerts", [{}])[0] if result.get("alerts") else {}
            results.append({
                "symbol": symbol,
                "top_signal": top_alert,
                "signal_count": len(result.get("ranked_signals", [])),
                "sentiment": result.get("sentiment_data", {}).get("overall_tone", "mixed"),
            })
        except Exception:
            results.append({"symbol": symbol, "error": "scan_failed"})
    return {"watchlist": results}
