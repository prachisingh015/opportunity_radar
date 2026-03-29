from celery import Celery
from celery.schedules import crontab
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "opportunity_radar",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.scan_tasks"],
)

celery_app.conf.beat_schedule = {
    # Scan top 50 NSE stocks every 30 minutes during market hours
    "scan-nse-top50": {
        "task": "tasks.scan_tasks.scan_watchlist",
        "schedule": crontab(minute="*/30", hour="9-15", day_of_week="1-5"),
    },
    # Full market scan at market open
    "morning-scan": {
        "task": "tasks.scan_tasks.full_market_scan",
        "schedule": crontab(hour=9, minute=15, day_of_week="1-5"),
    },
}

celery_app.conf.timezone = "Asia/Kolkata"
