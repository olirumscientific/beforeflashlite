import requests
from datetime import datetime

# Replace with your actual Render URL
URL = "https://renderbackend-t1iv.onrender.com/health"

def ping_server():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            print(f"[{datetime.now()}] Success! Server is awake.")
        else:
            print(f"[{datetime.now()}] Pinged, but got status code: {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] Ping failed: {e}")

if __name__ == "__main__":
    ping_server()