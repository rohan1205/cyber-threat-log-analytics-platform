from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List

from database.mongodb import get_logs_collection
from database.postgres import get_supabase_client
from ai.threat_scoring import score_threat
from ai.detection_rules import detect_threats

from auth.auth_routes import router as auth_router
from analytics.analytics_routes import router as analytics_router
from auth.auth_handler import get_current_user

app = FastAPI(
    title="Cyber Threat Log Analytics Platform",
    version="2.0.0"
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
    return {"status": "Backend running successfully", "version": "2.0.0"}

# ---------- LOG INGESTION (PRIVATE - STRICT MULTI-TENANCY) ----------
@app.post("/logs")
def create_log(log: dict, user_email: str = Depends(get_current_user)):
    """
    Create a log entry. Strictly filtered by user_email (owner field).
    """
    collection = get_logs_collection()

    # Set timestamp before saving
    log["timestamp"] = datetime.utcnow()
    log["owner"] = user_email  # CRITICAL: Tie this log to the user
    
    # Run threat scoring
    analysis = score_threat(log)
    log["severity"] = analysis["severity"]
    log["score"] = analysis["score"]
    log["reasons"] = analysis["reasons"]

    # Save log to MongoDB FIRST (detection rules query MongoDB)
    collection.insert_one(log)

    # Run real-time detection rules (will include the log we just saved)
    detected_alerts = detect_threats(log, user_email)
    
    # Store critical alerts in Supabase/PostgreSQL
    if detected_alerts:
        try:
            supabase = get_supabase_client()
            if supabase:
                for alert in detected_alerts:
                    # Only store HIGH and CRITICAL alerts
                    if alert["severity"] in ["HIGH", "CRITICAL"]:
                        supabase.table("alerts").insert({
                            "owner": user_email,
                            "alert_type": alert["alert_type"],
                            "severity": alert["severity"],
                            "description": alert["description"],
                            "source_ip": alert.get("source_ip"),
                            "metadata": {k: v for k, v in alert.items() if k not in ["alert_type", "severity", "description", "source_ip"]}
                        }).execute()
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error saving alert to Supabase: {e}")

    return {
        "message": "Log saved & threat scored",
        "analysis": analysis,
        "alerts_detected": len(detected_alerts) if detected_alerts else 0
    }

@app.get("/logs")
def get_logs(user_email: str = Depends(get_current_user)):
    """
    Get all logs for the current user. STRICT MULTI-TENANCY: Only returns logs where owner == user_email.
    """
    collection = get_logs_collection()
    # CRITICAL: Only find logs belonging to THIS user
    logs = list(collection.find({"owner": user_email}, {"_id": 0}).sort("timestamp", -1).limit(1000))
    return logs

# ---------- ALERTS ENDPOINT (STRICT MULTI-TENANCY) ----------
@app.get("/alerts")
def get_alerts(user_email: str = Depends(get_current_user)):
    """
    Fetch critical alerts from Supabase/PostgreSQL for the current user.
    STRICT MULTI-TENANCY: Only returns alerts where owner == user_email.
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []  # Return empty list if Supabase is not configured
        response = supabase.table("alerts").select("*").eq("owner", user_email).order("created_at", desc=True).limit(100).execute()
        return response.data
    except Exception as e:
        # Return empty list on error instead of raising exception
        print(f"Error fetching alerts: {e}")
        return []
