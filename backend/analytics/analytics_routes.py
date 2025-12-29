from fastapi import APIRouter, Depends
from database.mongodb import get_logs_collection
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/severity-count")
def severity_count(user=Depends(get_current_user)):
    collection = get_logs_collection()
    pipeline = [
        {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "severity": "$_id", "count": 1}}
    ]
    return list(collection.aggregate(pipeline))


@router.get("/top-events")
def top_events(limit: int = 5, user=Depends(get_current_user)):
    collection = get_logs_collection()
    pipeline = [
        {"$group": {"_id": "$event", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit},
        {"$project": {"_id": 0, "event": "$_id", "count": 1}}
    ]
    return list(collection.aggregate(pipeline))


@router.get("/recent-high-threats")
def recent_high_threats(limit: int = 5, user=Depends(get_current_user)):
    collection = get_logs_collection()
    return list(
        collection.find({"severity": "HIGH"})
        .sort("timestamp", -1)
        .limit(limit)
    )
