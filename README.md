
# 🛡️ Cyber Threat Log Analytics Platform

A **cloud-based cyber security backend platform** for ingesting, analyzing, and scoring system and network logs to detect suspicious activities and security threats using analytics and AI-based threat scoring.

This project simulates how **Security Operations Centers (SOC)** and **SIEM systems** process logs, prioritize threats, and surface actionable insights.

---

## 🚀 Key Features

### 🔐 Log Ingestion

* Accepts structured security logs via REST APIs
* Stores logs securely in **MongoDB Atlas (cloud)**

### 🧠 AI Threat Scoring

* Automatically assigns a **risk score (0–100)**
* Classifies threats into:

  * LOW
  * MEDIUM
  * HIGH
  * CRITICAL
* Provides **explainable reasons** for each score

### 📊 Security Analytics

* Severity distribution across logs
* Most frequent security events
* Recent high-risk and critical threats (SOC alerts)

### ☁️ Cloud & Scalable

* MongoDB Atlas (no local DB dependency)
* FastAPI backend with auto-generated documentation

---

## 🏗️ System Architecture

```
Client / Logs
      ↓
FastAPI Backend
      ↓
AI Threat Scoring Engine
      ↓
MongoDB Atlas (Cloud)
      ↓
Analytics APIs (SOC-style dashboards)
```

---

## 📌 API Endpoints

### 🔹 Core

* `GET /` → Health check
* `POST /logs` → Ingest a security log
* `GET /logs` → Retrieve stored logs

### 🔹 Analytics

* `GET /analytics/severity-count` → Count logs by severity
* `GET /analytics/top-events` → Most common security events
* `GET /analytics/recent-high-threats` → Latest high-risk threats

---

## 🧪 Example Log Input

```json
{
  "event": "multiple failed login attempts",
  "source_ip": "192.168.1.10"
}
```

### ✅ Example Output

```json
{
  "message": "Log saved & threat scored",
  "analysis": {
    "severity": "MEDIUM",
    "score": 60,
    "reasons": [
      "Failed action detected",
      "Login related event"
    ]
  }
}
```

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** MongoDB Atlas
* **AI Logic:** Rule-based threat scoring (extensible to ML)
* **Docs:** Swagger / OpenAPI
* **Version Control:** Git & GitHub

---

## 🔮 Future Enhancements

* Authentication & role-based access
* Real-time alerts (email / webhook)
* ML-based anomaly detection
* Frontend dashboard (React / Next.js)
* Log ingestion from files & streams

---

## 👨‍💻 Author

**Rohan Yadav**
B.Tech Student | Cyber Security | Backend & AI Enthusiast

---

## ⭐ Why This Project Matters

This project demonstrates:

* Real-world backend design
* Cyber security domain knowledge
* Data analytics & AI integration
* Cloud-native development

It is designed to reflect **industry-level SOC and SIEM backend systems**.

---

