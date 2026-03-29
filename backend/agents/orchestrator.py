"""
Opportunity Radar — Multi-Agent Orchestrator
Uses LangGraph to coordinate 5 specialized agents:
  1. FilingWatcher   — monitors exchange filings
  2. InsiderTracker  — detects insider trade clusters
  3. SentimentAnalyser — reads mgmt commentary tone
  4. SignalRanker    — scores signals by actionability
  5. AlertDispatcher — formats & pushes alerts
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
from agents.filing_watcher import filing_watcher_agent
from agents.insider_tracker import insider_tracker_agent
from agents.sentiment_analyser import sentiment_analyser_agent
from agents.signal_ranker import signal_ranker_agent
from agents.alert_dispatcher import alert_dispatcher_agent


class RadarState(TypedDict):
    stock_symbol: str
    raw_filings: List[dict]
    insider_trades: List[dict]
    sentiment_data: dict
    raw_signals: List[dict]
    ranked_signals: List[dict]
    alerts: List[dict]
    error: Optional[str]


def build_radar_graph() -> StateGraph:
    graph = StateGraph(RadarState)

    graph.add_node("filing_watcher", filing_watcher_agent)
    graph.add_node("insider_tracker", insider_tracker_agent)
    graph.add_node("sentiment_analyser", sentiment_analyser_agent)
    graph.add_node("signal_ranker", signal_ranker_agent)
    graph.add_node("alert_dispatcher", alert_dispatcher_agent)

    # Parallel data gathering → ranking → dispatch
    graph.set_entry_point("filing_watcher")
    graph.add_edge("filing_watcher", "insider_tracker")
    graph.add_edge("insider_tracker", "sentiment_analyser")
    graph.add_edge("sentiment_analyser", "signal_ranker")
    graph.add_edge("signal_ranker", "alert_dispatcher")
    graph.add_edge("alert_dispatcher", END)

    return graph.compile()


radar_graph = build_radar_graph()


async def run_radar(symbol: str) -> RadarState:
    """Run full radar pipeline for a given stock symbol."""
    initial_state: RadarState = {
        "stock_symbol": symbol,
        "raw_filings": [],
        "insider_trades": [],
        "sentiment_data": {},
        "raw_signals": [],
        "ranked_signals": [],
        "alerts": [],
        "error": None,
    }
    result = await radar_graph.ainvoke(initial_state)
    return result
