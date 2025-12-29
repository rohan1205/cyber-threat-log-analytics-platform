from fastapi import FastAPI
from datetime import datetime

from database.mongodb import get_logs_collection
from ai.threat_scoring import score_threat

app = FastAPI(title="Cyber Threat Log Analytics Platform")

@app.get("/")
def root():
    return {"status": "Backend running successfully"}

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
    logs = list(collection.find({}, {"_id": 0}))
    return logs
