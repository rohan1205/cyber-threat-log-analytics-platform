"""
Real-time threat detection rules for:
- DoS Attack: Same source_ip sends >10 logs in 10 seconds
- Port Scan: Same source_ip hits 5+ different ports in 1 minute
- Brute Force: 3+ 'Failed Login' events for the same user
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from database.mongodb import get_logs_collection


def check_dos_attack(source_ip: str, user_email: str, window_seconds: int = 10, threshold: int = 10) -> Optional[Dict]:
    """
    Check if the same source_ip sends more than threshold logs in window_seconds.
    Returns alert dict if detected, None otherwise.
    """
    collection = get_logs_collection()
    time_threshold = datetime.utcnow() - timedelta(seconds=window_seconds)
    
    # Count logs from this source_ip in the time window
    count = collection.count_documents({
        "owner": user_email,
        "source_ip": source_ip,
        "timestamp": {"$gte": time_threshold}
    })
    
    if count > threshold:
        return {
            "alert_type": "DoS Attack",
            "severity": "CRITICAL",
            "description": f"DoS attack detected: {source_ip} sent {count} requests in {window_seconds} seconds",
            "source_ip": source_ip,
            "count": count
        }
    return None


def check_port_scan(source_ip: str, user_email: str, destination_port: Optional[int], window_seconds: int = 60) -> Optional[Dict]:
    """
    Check if the same source_ip hits 5+ different ports in 1 minute.
    Returns alert dict if detected, None otherwise.
    """
    # Port scan detection requires destination_port to be present
    if destination_port is None:
        return None
        
    collection = get_logs_collection()
    time_threshold = datetime.utcnow() - timedelta(seconds=window_seconds)
    
    # Get all unique ports this source_ip hit in the time window
    pipeline = [
        {
            "$match": {
                "owner": user_email,
                "source_ip": source_ip,
                "timestamp": {"$gte": time_threshold},
                "destination_port": {"$exists": True, "$ne": None}
            }
        },
        {
            "$group": {
                "_id": "$destination_port"
            }
        }
    ]
    
    unique_ports = list(collection.aggregate(pipeline))
    unique_port_count = len(unique_ports)
    
    # If hit 5+ different ports in 1 minute, it's a port scan
    if unique_port_count >= 5:
        ports = [port["_id"] for port in unique_ports]
        return {
            "alert_type": "Port Scan",
            "severity": "HIGH",
            "description": f"Port scan detected: {source_ip} scanned {unique_port_count} different ports in {window_seconds} seconds (1 minute)",
            "source_ip": source_ip,
            "ports_scanned": ports[:10]  # Limit to first 10 ports
        }
    return None


def check_brute_force(source_ip: str, user_email: str, event: str, window_seconds: int = 300) -> Optional[Dict]:
    """
    Check if 3+ 'Failed Login' events occur from same source_ip.
    Returns alert dict if detected, None otherwise.
    """
    event_lower = event.lower()
    if "failed login" not in event_lower and "failed login attempt" not in event_lower:
        return None
    
    collection = get_logs_collection()
    time_threshold = datetime.utcnow() - timedelta(seconds=window_seconds)
    
    # Count failed login events from this source_ip in the time window
    failed_login_count = collection.count_documents({
        "owner": user_email,
        "source_ip": source_ip,
        "timestamp": {"$gte": time_threshold},
        "event": {"$regex": "failed login", "$options": "i"}
    })
    
    # If 3+ failed login attempts, it's brute force
    if failed_login_count >= 3:
        return {
            "alert_type": "Brute Force",
            "severity": "HIGH",
            "description": f"Brute force attack detected: {source_ip} attempted {failed_login_count} failed logins in {window_seconds} seconds",
            "source_ip": source_ip,
            "failed_attempts": failed_login_count
        }
    return None


def detect_threats(log: dict, user_email: str) -> List[Dict]:
    """
    Run all detection rules and return list of detected alerts.
    """
    alerts = []
    source_ip = log.get("source_ip")
    destination_port = log.get("destination_port")
    event = log.get("event", "")
    
    if not source_ip:
        return alerts
    
    # Check DoS Attack
    dos_alert = check_dos_attack(source_ip, user_email)
    if dos_alert:
        alerts.append(dos_alert)
    
    # Check Port Scan
    port_scan_alert = check_port_scan(source_ip, user_email, destination_port)
    if port_scan_alert:
        alerts.append(port_scan_alert)
    
    # Check Brute Force
    brute_force_alert = check_brute_force(source_ip, user_email, event)
    if brute_force_alert:
        alerts.append(brute_force_alert)
    
    return alerts

