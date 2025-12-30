from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from database.mongodb import get_logs_collection
from auth.auth_handler import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/severity-count")
def severity_count(user_email: str = Depends(get_current_user)):
    """
    Get count of logs by severity for the current user.
    STRICT MULTI-TENANCY: Only includes logs where owner == user_email.
    """
    collection = get_logs_collection()
    pipeline = [
        {
            "$match": { "owner": user_email }
        },
        {
            "$project": {
                "severity": {
                    "$toUpper": {
                        "$ifNull": ["$severity", "UNKNOWN"]
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$severity",
                "count": { "$sum": 1 }
            }
        }
    ]

    return list(collection.aggregate(pipeline))

@router.get("/time-series")
def time_series(user_email: str = Depends(get_current_user), hours: int = 24):
    """
    Get time-series data for the last N hours.
    STRICT MULTI-TENANCY: Only includes logs where owner == user_email.
    Returns data grouped by hour.
    """
    collection = get_logs_collection()
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    pipeline = [
        {
            "$match": {
                "owner": user_email,
                "timestamp": {"$gte": time_threshold}
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d %H:00:00",
                        "date": "$timestamp"
                    }
                },
                "count": { "$sum": 1 },
                "avg_score": { "$avg": "$score" }
            }
        },
        {
            "$sort": { "_id": 1 }
        }
    ]
    
    return list(collection.aggregate(pipeline))

@router.get("/top-threats")
def top_threats(user_email: str = Depends(get_current_user), limit: int = 10):
    """
    Get top threats by score.
    STRICT MULTI-TENANCY: Only includes logs where owner == user_email.
    """
    collection = get_logs_collection()
    
    pipeline = [
        {
            "$match": {
                "owner": user_email,
                "severity": { "$in": ["HIGH", "CRITICAL"] }
            }
        },
        {
            "$sort": { "score": -1, "timestamp": -1 }
        },
        {
            "$limit": limit
        },
        {
            "$project": {
                "_id": 0,
                "event": 1,
                "source_ip": 1,
                "severity": 1,
                "score": 1,
                "timestamp": 1,
                "reasons": 1
            }
        }
    ]
    
    return list(collection.aggregate(pipeline))

@router.get("/source-ip-stats")
def source_ip_stats(user_email: str = Depends(get_current_user)):
    """
    Get statistics by source IP.
    STRICT MULTI-TENANCY: Only includes logs where owner == user_email.
    """
    collection = get_logs_collection()
    
    pipeline = [
        {
            "$match": {
                "owner": user_email,
                "source_ip": { "$exists": True, "$ne": None }
            }
        },
        {
            "$group": {
                "_id": "$source_ip",
                "count": { "$sum": 1 },
                "avg_score": { "$avg": "$score" },
                "max_severity": { "$max": "$severity" }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": 20
        }
    ]
    
    return list(collection.aggregate(pipeline))
