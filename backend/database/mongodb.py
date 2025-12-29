from pymongo import MongoClient

MONGO_URI = "mongodb+srv://rohanydv1305:rohanydv1305@cluster0.2xfh4vd.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["cyber_logs"]

def get_logs_collection():
    return db["logs"]
