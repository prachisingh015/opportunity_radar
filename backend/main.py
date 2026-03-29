from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import signals, stocks, alerts, health
from services.websocket_manager import ws_manager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Opportunity Radar API starting...")
    yield
    # Shutdown
    print("🛑 Shutting down...")

app = FastAPI(
    title="Opportunity Radar API",
    description="AI-powered stock signal detection for Indian retail investors",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except Exception:
        ws_manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
