    import csv
import requests
import time

# --- CONFIGURATION ---
API_URL = "https://cyber-threat-log-analytics-platform.onrender.com/logs"
# PASTE YOUR TOKEN BELOW
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwiZXhwIjoxNzY3MTEzMTM2fQ.HLG_5zL163zATXi-Xg7eBahLow6cs1HRM19bKWTY8yA"

def send_logs():
    with open('logs.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            payload = {
                "event": row['event'],
                "severity": "MEDIUM" if "DDoS" in row['event'] or "SSH" in row['event'] else "LOW",
                "source_ip": row['source_ip']
            }
            
            headers = {"Authorization": f"Bearer {TOKEN}"}
            
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                print(f"Sent: {row['event']} | Status: {response.status_code}")
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(1) # Sends 1 log every second

if __name__ == "__main__":
    send_logs()