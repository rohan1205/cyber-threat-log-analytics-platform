from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from database.mongodb import get_logs_collection

router = APIRouter()

@router.get("/severity-count")
def severity_count(current_user: dict = Depends(get_current_user)):
    collection = get_logs_collection()

    pipeline = [
        {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "severity": "$_id", "count": 1}}
    ]

    return list(collection.aggregate(pipeline))
