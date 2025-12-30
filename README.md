# 🛡️ Cyber-Sentry: Cloud-Based Threat Monitoring & Log Analytics Platform

Cyber-Sentry is a **full-stack, cloud-native Security Operations Center (SOC) platform** designed to ingest, analyze, score, and visualize system and network security logs in real time.

It simulates how **enterprise SOC & SIEM systems** collect telemetry, detect threats, prioritize incidents, and surface actionable security insights for analysts.

---

## 🚀 Live Demo

* **Security Dashboard (Frontend)**
  👉 [https://cyber-threat-log-analytics-platform-ten.vercel.app](https://cyber-threat-log-analytics-platform-ten.vercel.app)

* **Backend API (FastAPI)**
  👉 [https://cyber-threat-log-analytics-platform.onrender.com](https://cyber-threat-log-analytics-platform.onrender.com)

---

## 🧠 Problem Statement

Modern systems generate **massive volumes of security logs** every second. Without a centralized intelligence layer, critical attacks such as:

* Distributed Denial of Service (DoS)
* Brute Force login attempts
* Port Scanning activities

often go **undetected or unprioritized**.

---

## 💡 Solution

Cyber-Sentry acts as a **central security brain** by:

* Providing a secure ingestion pipeline for logs
* Applying **heuristic & pattern-based threat detection**
* Assigning **risk scores and severity levels**
* Visualizing insights on a modern, interactive SOC dashboard

---

## 🏗️ System Architecture

```
Client / Log Sources
        ↓
FastAPI Ingestion Layer
        ↓
Threat Detection & Scoring Engine
        ↓
MongoDB Atlas (Raw Logs)
        ↓
Supabase / PostgreSQL (Critical Alerts)
        ↓
Analytics APIs
        ↓
React Security Dashboard (SOC View)
```

---

## 🛠️ Full Tech Stack

### 🔧 Backend (The Intelligence Layer)

* Python – FastAPI
* JWT Authentication + OAuth2
* Custom Threat Detection Engine
* Asynchronous APIs
* Swagger / OpenAPI Documentation
* Hosted on Render

### 🎛️ Frontend (The Command Center)

* React 18 + Vite
* Tailwind CSS (Glassmorphism UI)
* Framer Motion (Smooth animations)
* Recharts (Area, Bar & Pie charts)
* Lucide React (Icons)
* Hosted on Vercel

### 🗄️ Database & Cloud

* MongoDB Atlas – High-volume raw security logs
* Supabase (PostgreSQL) – Persistent critical alerts
* Cloud-native, scalable architecture

---

## ⚙️ Key Features

### 🔐 Log Ingestion

* Accepts structured security logs via REST APIs
* Stores data securely in MongoDB Atlas

### 🧠 AI-Based Threat Scoring

* Assigns a **risk score (0–100)**
* Classifies threats into:

  * LOW
  * MEDIUM
  * HIGH
  * CRITICAL
* Provides **explainable reasons** for each score

### 🔍 Real-Time Threat Detection

* **DoS Detection**: Flags IPs sending >10 requests within 10 seconds
* **Port Scan Detection**: Detects IPs hitting 5+ unique ports rapidly
* **Brute Force Detection**: Identifies repeated authentication failures

### 📊 Security Analytics Dashboard

* Severity distribution charts
* Most frequent attack types
* Recent high-risk & critical SOC alerts
* Live telemetry feed (SOC-style console)

### 🧩 Multi-Tenant Architecture

* Each user has a **private security workspace**
* Logs and alerts are isolated using JWT-based ownership filtering

### 🧪 Attack Simulator

* Simulate DoS, brute force, and scan attacks
* Test detection rules end-to-end

---

## 📡 API Endpoints

### 🔹 Authentication

| Method | Endpoint              | Description          | Auth   |
| ------ | --------------------- | -------------------- | ------ |
| POST   | `/auth/auth/register` | Register new analyst | Public |
| POST   | `/auth/auth/login`    | Login & receive JWT  | Public |

### 🔹 Logs

| Method | Endpoint | Description         | Auth |
| ------ | -------- | ------------------- | ---- |
| POST   | `/logs`  | Ingest security log | JWT  |
| GET    | `/logs`  | Retrieve user logs  | JWT  |

### 🔹 Analytics

| Method | Endpoint                         | Description               | Auth |
| ------ | -------------------------------- | ------------------------- | ---- |
| GET    | `/analytics/severity-count`      | Count threats by severity | JWT  |
| GET    | `/analytics/top-events`          | Most frequent events      | JWT  |
| GET    | `/analytics/recent-high-threats` | Latest high-risk alerts   | JWT  |

---

## 🧪 Example Log Input

```json
{
  "event": "multiple failed login attempts",
  "source_ip": "192.168.1.10"
}
```

### ✅ Example Threat Analysis Output

```json
{
  "message": "Log saved & threat scored",
  "analysis": {
    "severity": "MEDIUM",
    "score": 60,
    "reasons": [
      "Failed authentication detected",
      "Login-related suspicious activity"
    ]
  }
}
```

---

## 🚀 Installation & Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔮 Future Enhancements

* Role-based access control (SOC roles)
* Real-time alerts (Email / Webhooks)
* ML-based anomaly detection
* Log ingestion from files & streams
* Advanced dashboards & timelines

---

## 👨‍💻 Author

**Rohan Yadav**
B.Tech Student | Cyber Security | Full-Stack Developer

* LinkedIn: [https://www.linkedin.com/in/rohan-yadav-433601313/](https://www.linkedin.com/in/rohan-yadav-433601313/)
* GitHub: [https://github.com/rohan1205](https://github.com/rohan1205)

---

## ⭐ Why This Project Matters

This project demonstrates:

* Industry-grade backend design
* SOC & SIEM domain understanding
* Cloud-native development
* Security-first architecture
* Data analytics & visualization
* Full-stack system thinking

Cyber-Sentry is not just a dashboard — it is a **complete security intelligence pipeline**.

🛡️ Built to reflect real-world SOC systems.
🚀 Successfully deployed & fully operational.
