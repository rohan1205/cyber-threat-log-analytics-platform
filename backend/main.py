from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from auth.auth_routes import router as auth_router
from analytics.analytics_routes import router as analytics_router
from database.mongodb import get_logs_collection
from ai.threat_scoring import score_threat

app = FastAPI(
    title="Cyber Threat Log Analytics Platform",
    version="1.0.0"
)

# CORS (safe to keep open)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running successfully"}

# Routers
app.include_router(auth_router)
app.include_router(analytics_router)

# Logs
@app.post("/logs")
def create_log(log: dict):
    collection = get_logs_collection()
    analysis = score_threat(log)

    log.update({
        "severity": analysis["severity"],
        "score": analysis["score"],
        "reasons": analysis["reasons"],
        "timestamp": datetime.utcnow()
    })

    collection.insert_one(log)
    return {"message": "Log saved", "analysis": analysis}

@app.get("/logs")
def get_logs():
    collection = get_logs_collection()
    return list(collection.find({}, {"_id": 0}))
