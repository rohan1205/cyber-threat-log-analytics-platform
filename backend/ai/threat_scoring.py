def score_threat(log: dict):
    score = 0
    reasons = []

    event = log.get("event", "").lower()

    if "failed" in event:
        score += 30
        reasons.append("Failed action detected")

    if "login" in event:
        score += 30
        reasons.append("Login related event")

    if "brute" in event or "attack" in event:
        score += 40
        reasons.append("Attack keyword detected")

    if score >= 70:
        severity = "HIGH"
    elif score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "severity": severity,
        "score": score,
        "reasons": reasons
    }
