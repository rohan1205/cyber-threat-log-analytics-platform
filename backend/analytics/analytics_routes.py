from fastapi import APIRouter, Depends
from database.mongodb import collection
from auth.auth_handler import get_current_user  # Dependency to get the logged-in user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/severity-count")
def severity_count(user_email: str = Depends(get_current_user)):
    pipeline = [
        # 1. NEW: Filter documents to only include those belonging to the current user
        {
            "$match": { "owner": user_email }
        },
        # 2. Normalize severity to uppercase and handle nulls
        {
            "$project": {
                "severity": {
                    "$toUpper": {
                        "$ifNull": ["$severity", "UNKNOWN"]
                    }
                }
            }
        },
        # 3. Group by the normalized severity
        {
            "$group": {
                "_id": "$severity",
                "count": { "$sum": 1 }
            }
        }
        # NOTE: We removed the final $project so that the output remains 
        # as {"_id": "HIGH", "count": 5}, which matches your React frontend logic.
    ]

    return list(collection.aggregate(pipeline))