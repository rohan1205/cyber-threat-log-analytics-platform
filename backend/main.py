from fastapi import FastAPI, Depends  # Add Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from database.mongodb import get_logs_collection
from ai.threat_scoring import score_threat

from auth.auth_routes import router as auth_router
from analytics.analytics_routes import router as analytics_router
# IMPORT the dependency that extracts the user from the token
from auth.auth_handler import get_current_user 

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

# ---------- LOG INGESTION (NOW PRIVATE) ----------
@app.post("/logs")
def create_log(log: dict, user_email: str = Depends(get_current_user)): # Added Auth
    collection = get_logs_collection()

    analysis = score_threat(log)

    log["owner"] = user_email  # <--- CRITICAL: Tie this log to the user
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
def get_logs(user_email: str = Depends(get_current_user)): # Added Auth
    collection = get_logs_collection()
    # <--- CRITICAL: Only find logs belonging to THIS user
    return list(collection.find({"owner": user_email}, {"_id": 0}))