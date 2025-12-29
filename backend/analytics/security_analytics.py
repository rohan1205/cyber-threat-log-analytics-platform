from database.mongodb import get_logs_collection

def severity_count():
    collection = get_logs_collection()

    pipeline = [
        {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "severity": "$_id", "count": 1}}
    ]

    return list(collection.aggregate(pipeline))


def top_events(limit: int = 5):
    collection = get_logs_collection()

    pipeline = [
        {"$group": {"_id": "$event", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit},
        {"$project": {"_id": 0, "event": "$_id", "count": 1}}
    ]

    return list(collection.aggregate(pipeline))


def recent_high_threats(limit: int = 5):
    collection = get_logs_collection()

    return list(
        collection.find(
            {"severity": "HIGH"},
            {"_id": 0}
        )
        .sort("timestamp", -1)
        .limit(limit)
    )
