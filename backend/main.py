from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from database.mongodb import get_logs_collection
from ai.threat_scoring import score_threat

from auth.auth_routes import router as auth_router
from analytics.analytics_routes import router as analytics_router

app = FastAPI(
    title="Cyber Threat Log Analytics Platform",
    version="1.0.0"
)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- ROUTERS ----------
app.include_router(auth_router, prefix="/auth")
app.include_router(analytics_router, prefix="/analytics")

# ---------- ROOT ----------
@app.get("/")
def root():
    return {"status": "Backend running successfully"}

# ---------- LOG INGESTION ----------
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
