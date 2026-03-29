from fastapi import APIRouter, HTTPException
import yfinance as yf

router = APIRouter()


def nse_ticker(symbol: str) -> str:
    return f"{symbol}.NS"


@router.get("/{symbol}/quote")
async def get_quote(symbol: str):
    """Get current price, change, volume for a stock."""
    try:
        ticker = yf.Ticker(nse_ticker(symbol.upper()))
        info = ticker.fast_info
        hist = ticker.history(period="2d")
        if hist.empty:
            raise HTTPException(status_code=404, detail="Stock not found")

        prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else hist["Close"].iloc[-1]
        curr_close = hist["Close"].iloc[-1]
        change = curr_close - prev_close
        change_pct = (change / prev_close) * 100

        return {
            "symbol": symbol.upper(),
            "price": round(curr_close, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "volume": int(hist["Volume"].iloc[-1]),
            "high_52w": round(getattr(info, "year_high", 0), 2),
            "low_52w": round(getattr(info, "year_low", 0), 2),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/history")
async def get_history(symbol: str, period: str = "3mo"):
    """Get OHLCV history for charting."""
    try:
        ticker = yf.Ticker(nse_ticker(symbol.upper()))
        hist = ticker.history(period=period)
        if hist.empty:
            raise HTTPException(status_code=404, detail="No data found")

        candles = [
            {
                "date": str(idx.date()),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
                "volume": int(row["Volume"]),
            }
            for idx, row in hist.iterrows()
        ]
        return {"symbol": symbol.upper(), "candles": candles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_stocks(q: str):
    """Search NSE stocks by name/symbol."""
    # Top NSE stocks for demo — in production, use NSE search API
    nse_stocks = [
        {"symbol": "RELIANCE", "name": "Reliance Industries Ltd"},
        {"symbol": "TCS", "name": "Tata Consultancy Services"},
        {"symbol": "INFY", "name": "Infosys Ltd"},
        {"symbol": "HDFCBANK", "name": "HDFC Bank Ltd"},
        {"symbol": "BAJFINANCE", "name": "Bajaj Finance Ltd"},
        {"symbol": "WIPRO", "name": "Wipro Ltd"},
        {"symbol": "TATAMOTORS", "name": "Tata Motors Ltd"},
        {"symbol": "ADANIENT", "name": "Adani Enterprises Ltd"},
        {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical"},
        {"symbol": "ICICIBANK", "name": "ICICI Bank Ltd"},
        {"symbol": "HINDUNILVR", "name": "Hindustan Unilever Ltd"},
        {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank"},
    ]
    q_upper = q.upper()
    filtered = [
        s for s in nse_stocks
        if q_upper in s["symbol"] or q.lower() in s["name"].lower()
    ]
    return {"results": filtered[:8]}
