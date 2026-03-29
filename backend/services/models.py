from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Signal(Base):
    __tablename__ = "signals"

    id = Column(String, primary_key=True)
    symbol = Column(String(20), nullable=False, index=True)
    headline = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    tag = Column(String(50))
    direction = Column(String(10))  # bullish | bearish | neutral
    score = Column(Integer, default=0)
    urgency = Column(String(20))  # today | this_week | this_month
    confluence = Column(Boolean, default=False)
    raw_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ScanLog(Base):
    __tablename__ = "scan_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), nullable=False)
    agents_run = Column(JSON)
    signals_found = Column(Integer, default=0)
    duration_ms = Column(Float)
    status = Column(String(20))  # success | failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
