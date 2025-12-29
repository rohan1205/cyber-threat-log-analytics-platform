from fastapi import FastAPI
from datetime import datetime

from database.mongodb import get_logs_collection
from ai.threat_scoring import score_threat
from analytics.security_analytics import (
    severity_count,
    top_events,
    recent_high_threats
)

app = FastAPI(title="Cyber Threat Log Analytics Platform")

# ---------------- BASIC ----------------

@app.get("/")
def root():
    return {"status": "Backend running successfully"}

# ---------------- LOG INGESTION ----------------

@app.post("/logs")
def create_log(log: dict):
    collection = get_logs_collection()

    analysis = score_threat(log)

    log["severity"] = analysis["severity"]
    log["score"] = analysis["score"]
    log["reasons"] = analysis["reasons"]
    log["timestamp"] = datetime.utcnow()

    collection.insert_one(log)

    return {
        "message": "Log saved & threat scored",
        "analysis": analysis
    }

@app.get("/logs")
def get_logs():
    collection = get_logs_collection()
    return list(collection.find({}, {"_id": 0}))

# ---------------- ANALYTICS (SIEM STYLE) ----------------

@app.get("/analytics/severity-count")
def analytics_severity_count():
    return severity_count()

@app.get("/analytics/top-events")
def analytics_top_events(limit: int = 5):
    return top_events(limit)

@app.get("/analytics/recent-high-threats")
def analytics_recent_high_threats(limit: int = 5):
    return recent_high_threats(limit)
