from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Database
from database.mongodb import get_logs_collection

# AI
from ai.threat_scoring import score_threat

# Routers
from auth.auth_routes import router as auth_router
from analytics.analytics_routes import router as analytics_router

app = FastAPI(
    title="Cyber Threat Log Analytics Platform",
    version="1.0.0"
)

# -------------------- CORS (FIXED) --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:8080",
        "http://localhost",
        "https://cyber-threat-log-analytics-platform.onrender.com",
    ],
    allow_credentials=False,  # ✅ IMPORTANT FIX
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- ROUTERS --------------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])

# -------------------- ROOT --------------------
@app.get("/")
def root():
    return {"status": "Backend running successfully"}

# -------------------- LOG APIs --------------------
@app.post("/logs")
def create_log(log: dict):
    collection = get_logs_collection()
    analysis = score_threat(log)
    log["analysis"] = analysis
    collection.insert_one(log)
    return {"message": "Log saved & threat scored", "analysis": analysis}

@app.get("/logs")
def get_logs(limit: int = 50):
    collection = get_logs_collection()
    return list(collection.find({}, {"_id": 0}).limit(limit))
