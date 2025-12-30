
🛡️ Cyber-Sentry: Cloud-Based Threat Monitoring & Log Analytics
Cyber-Sentry is a high-performance, full-stack security platform designed to collect, analyze, and visualize network security logs in real-time. Built with a focus on Multi-Tenancy and Pattern-Based Threat Detection, the platform transforms raw log data into actionable security intelligence.
🚀 Live Demo
Dashboard: cyber-threat-log-analytics-platform-ten.vercel.app
Backend API: cyber-threat-log-analytics-platform.onrender.com
🧠 The Problem
In modern infrastructure, security logs are generated at a massive scale. Without a centralized "brain" to analyze these logs, critical attacks like DoS, Port Scans, and Brute Force attempts often go unnoticed.
💡 The Solution
Cyber-Sentry provides a secure ingestion point for logs, analyzes them using a custom threat-scoring engine, and visualizes the results on a modern, animated dashboard.
🛠️ Tech Stack
Backend (The Intelligence)
Framework: Python / FastAPI
Security: JWT (JSON Web Tokens) with OAuth2
Data Logic: Custom Pattern-Matching Detection Engine
Hosting: Render
Frontend (The Command Center)
Framework: React 18 (Vite)
Styling: Tailwind CSS (Glassmorphism UI)
Animations: Framer Motion
Charts: Recharts (Area, Bar, and Pie distributions)
Hosting: Vercel
Database (The Memory)
NoSQL: MongoDB Atlas (High-volume log storage)
SQL: Supabase / PostgreSQL (Persistent critical alerts)
⚙️ Key Features
Multi-Tenant Architecture: Every user has a private data environment. Logs sent by User A are never visible to User B.
Real-Time Threat Detection:
DoS Detection: Identifies >10 requests from a single IP within a 10-second window.
Port Scan Detection: Flags IPs hitting 5+ unique ports in a short duration.
Brute Force Detection: Monitors for repeated 'Failed Login' events.
Interactive Security Dashboard:
Visual distribution of severity (Low, Medium, High).
Live System Console showing a stream of inbound telemetry.
Area charts for traffic volume analysis.
Attack Simulator: A built-in tool to simulate attacks (DoS, Brute Force, Scans) and test detection rules.
🚀 Installation & Setup
Backend
Navigate to /backend:
code
Bash
pip install -r requirements.txt
uvicorn main:app --reload
Frontend
Navigate to /frontend:
code
Bash
npm install
npm run dev
📡 API Endpoints
Method	Endpoint	Description	Auth
POST	/auth/auth/register	Create a new security analyst account.	No
POST	/auth/auth/login	Authenticate and receive a JWT token.	No
POST	/logs	Ingest a new security log.	JWT
GET	/analytics/severity-count	Fetch count of threats by severity.	JWT
GET	/logs	Retrieve the live log feed for the user.	JWT
🛡️ Detection Logic Example
code
Python
# Logic implemented in the backend to flag high-risk activity
if logs_in_last_10_seconds > 10:
    severity = "HIGH"
    event = "Potential DoS Attack"

if unique_ports_hit > 5:
    severity = "MEDIUM"
    event = "Port Scanning Detected"
👤 Author
Rohan Yadav
Cyber Security Enthusiast & Full-Stack Developer
LinkedIn Profile
GitHub
🌟 Project Status: Successfully Deployed & Operational 🚀
Final Pro-Tip for your GitHub:
Make sure you take a screenshot of your dashboard and name it dashboard.png. Then add this line to the top of your README to make it look even better:
![Dashboard Screenshot](./dashboard.png)
You're officially done! You should be very proud of this. 🛡️🏆
User
🛡️ Cyber Threat Log Analytics Platform
A cloud-based cyber security backend platform for ingesting, analyzing, and scoring system and network logs to detect suspicious activities and security threats using analytics and AI-based threat scoring.
This project simulates how Security Operations Centers (SOC) and SIEM systems process logs, prioritize threats, and surface actionable insights.
🚀 Key Features
🔐 Log Ingestion
Accepts structured security logs via REST APIs
Stores logs securely in MongoDB Atlas (cloud)
🧠 AI Threat Scoring
Automatically assigns a risk score (0–100)
Classifies threats into:
LOW
MEDIUM
HIGH
CRITICAL
Provides explainable reasons for each score
📊 Security Analytics
Severity distribution across logs
Most frequent security events
Recent high-risk and critical threats (SOC alerts)
☁️ Cloud & Scalable
MongoDB Atlas (no local DB dependency)
FastAPI backend with auto-generated documentation
🏗️ System Architecture
code
Code
Client / Logs
      ↓
FastAPI Backend
      ↓
AI Threat Scoring Engine
      ↓
MongoDB Atlas (Cloud)
      ↓
Analytics APIs (SOC-style dashboards)
📌 API Endpoints
🔹 Core
GET / → Health check
POST /logs → Ingest a security log
GET /logs → Retrieve stored logs
🔹 Analytics
GET /analytics/severity-count → Count logs by severity
GET /analytics/top-events → Most common security events
GET /analytics/recent-high-threats → Latest high-risk threats
🧪 Example Log Input
code
JSON
{
  "event": "multiple failed login attempts",
  "source_ip": "192.168.1.10"
}
✅ Example Output
code
JSON
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
🛠️ Tech Stack
Backend: FastAPI (Python)
Database: MongoDB Atlas
AI Logic: Rule-based threat scoring (extensible to ML)
Docs: Swagger / OpenAPI
Version Control: Git & GitHub
🔮 Future Enhancements
Authentication & role-based access
Real-time alerts (email / webhook)
ML-based anomaly detection
Frontend dashboard (React / Next.js)
Log ingestion from files & streams
👨‍💻 Author
Rohan Yadav
B.Tech Student | Cyber Security | Backend & AI Enthusiast
⭐ Why This Project Matters
This project demonstrates:
Real-world backend design
Cyber security domain knowledge
Data analytics & AI integration
Cloud-native development
It is designed to reflect industry-level SOC and SIEM backend systems.
this was previous one polish this one and add tech stacks used properlyyyyyy
Model
ThinkingThoughts
Expand to view model thoughts

chevron_right
This is a polished, Senior-Level README that accurately reflects the full-stack, multi-tenant architecture you have actually built. It highlights the advanced security logic, the "Glassmorphism" UI, and the dual-database strategy (SQL + NoSQL) that recruiters love to see.
🛡️ Cyber-Sentry: Enterprise Threat Monitoring & Log Analytics
Cyber-Sentry is a professional-grade, full-stack Security Operations Center (SOC) platform. It provides a centralized "Command Center" for ingesting, analyzing, and visualizing network security telemetry in real-time. By utilizing Heuristic Pattern Matching and Dual-Cloud Storage, it detects and alerts on critical threats like DoS, Port Scans, and Brute Force attacks.
🚀 Live Infrastructure
Security Dashboard: cyber-threat-log-analytics-platform-ten.vercel.app
Intelligence API: cyber-threat-log-analytics-platform.onrender.com
LinkedIn: Rohan Yadav
🏗️ Technical Architecture
The platform follows a modern Monorepo structure with a clean separation of concerns:
code
Text
Log Telemetry → FastAPI Ingestion → Heuristic Detection Engine → MongoDB (Raw Logs)
                                                                ↘ Supabase (Alerts)
                                                                        ↓
React Dashboard ← JWT Authenticated API Calls ← Framer Motion & Recharts Visualization
🛠️ Full-Stack Tech Stack
Frontend (The Command Center)
React 18 & Vite: Ultra-fast, component-based UI.
Tailwind CSS: Custom Glassmorphism theme with deep-slate aesthetics.
Framer Motion: Smooth, hardware-accelerated animations for real-time telemetry updates.
Recharts: Interactive Area, Bar, and Pie charts for security trend analysis.
Lucide React: Professional iconography for security metrics.
Backend (The Intelligence)
FastAPI (Python): High-performance asynchronous API framework.
JWT & OAuth2: Secure, stateless session management with hashed credentials.
Multi-Tenancy Logic: Strict data isolation using "Owner-Based" filtering in all DB queries.
Detection Engine: Custom logic for identifying DoS, Brute Force, and Port Scans.
Database & Cloud (The Memory)
MongoDB Atlas: Distributed NoSQL storage for high-volume raw security logs.
Supabase (PostgreSQL): Relational storage for persistent, mission-critical security alerts.
Vercel: Frontend hosting with Global Edge Network.
Render: Automated CI/CD backend deployment.
⚙️ Advanced Features
🔍 Real-Time Threat Detection Rules
Unlike basic logging tools, Cyber-Sentry implements active detection heuristics:
DoS Mitigation: Flags any source IP exceeding 10 requests within a 10-second window.
Port Scan Intelligence: Detects vertical scanning (one IP hitting 5+ unique ports).
Brute Force Detection: Monitors for sequential authentication failures.
🔐 Private Security Sessions
Implemented Multi-Tenant Privacy. Every security analyst has an isolated workspace. Using JWT claims, the backend ensures that logs and alerts are only visible to the user who generated or ingested them.
💻 Live SOC Console
Includes a terminal-style "Live Feed" that streams inbound security telemetry, providing a real-time view of network activity as it hits the ingestion point.
📡 API Documentation (Endpoints)
Method	Endpoint	Description	Security
POST	/auth/auth/register	Register a new security analyst.	Public
POST	/auth/auth/login	Authenticate and receive JWT access token.	Public
POST	/logs	Ingest new log telemetry for analysis.	JWT Restricted
GET	/analytics/severity-count	Aggregate threat counts for dashboard charts.	JWT Restricted
GET	/logs	Retrieve filtered log history for current user.	JWT Restricted
👨‍💻 Author
Rohan Yadav
B.Tech Student | Cyber Security | Full-Stack Developer
"This project demonstrates my ability to bridge the gap between low-level security logic and high-level cloud architecture. It reflects industry-level SOC and SIEM backend systems built with a focus on speed, security, and scalability."
🧪 Example Threat Scoring Output
code
JSON
{
  "event": "Potential DoS Attack",
  "analysis": {
    "severity": "HIGH",
    "score": 85,
    "reasons": [
      "High frequency request pattern",
      "Source IP saturation"
    ]
  }
}
⭐ Why This Project Matters
This platform isn't just a dashboard; it’s a complete pipeline. It demonstrates:
Cloud-Native Development: Fully serverless and cloud-hosted.
Security-First Mindset: Implementation of JWT, Password Hashing, and CORS.
Data Engineering: Using MongoDB Aggregation Pipelines to process security data.
UX Design: Creating complex data visualizations that are easy to understand.
