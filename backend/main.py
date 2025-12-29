from fastapi import FastAPI
from database.mongodb import get_logs_collection
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Backend running successfully"}

@app.post("/logs")
def create_log(log: dict):
    collection = get_logs_collection()
    log["timestamp"] = datetime.utcnow()
    collection.insert_one(log)
    return {"message": "Log saved successfully"}

@app.get("/logs")
def get_logs():
    collection = get_logs_collection()
    logs = list(collection.find({}, {"_id": 0}))
    return logs
