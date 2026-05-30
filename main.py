import os
import json
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request
import requests
import webbrowser
import threading

from whoop import get_whoop_data
from ai import generate_summary
from email_sender import send_email

load_dotenv()

CLIENT_ID = os.getenv("WHOOP_CLIENT_ID")
CLIENT_SECRET = os.getenv("WHOOP_CLIENT_SECRET")
REDIRECT_URI = os.getenv("WHOOP_REDIRECT_URI")
TOKENS_FILE = "C:/whoop-agent/tokens.json"
NOTES_FILE = "C:/whoop-agent/notes.txt"

app = Flask(__name__)

# ─── OAuth ───────────────────────────────────────────

def get_auth_url():
    scope = "read:recovery read:cycles read:sleep read:workout read:profile read:body_measurement offline"
    return (
        f"https://api.prod.whoop.com/oauth/oauth2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={scope.replace(' ', '%20')}"
        f"&state=12345678"
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")
    response = requests.post(
        "https://api.prod.whoop.com/oauth/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
    )
    tokens = response.json()
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    print("Token saved!")
    return "Authentication successful! You can close this tab."

def refresh_token():
    with open(TOKENS_FILE) as f:
        tokens = json.load(f)
    response = requests.post(
        "https://api.prod.whoop.com/oauth/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
    )
    new_tokens = response.json()
    with open(TOKENS_FILE, "w") as f:
        json.dump(new_tokens, f, indent=2)
    print("Token refreshed!")
    return new_tokens["access_token"]

def get_access_token():
    with open(TOKENS_FILE) as f:
        tokens = json.load(f)
    return tokens["access_token"]

# ─── Notes ───────────────────────────────────────────

def read_notes():
    if not os.path.exists(NOTES_FILE):
        return "No notes recorded today."
    with open(NOTES_FILE) as f:
        content = f.read().strip()
    return content if content else "No notes recorded today."

def clear_notes():
    with open(NOTES_FILE, "w") as f:
        f.write("")
    print("Notes cleared for tomorrow!")

# ─── Daily Job ───────────────────────────────────────

def daily_job():
    print(f"\n Running daily job at {datetime.now()}")
    
    try:
        # Refresh token first
        token = refresh_token()
    except:
        token = get_access_token()

    print("Fetching WHOOP data...")
    whoop_data = get_whoop_data(token)
    
    print("Reading notes...")
    notes = read_notes()
    
    print("Generating AI summary...")
    summary = generate_summary(whoop_data, notes)
    
    print("Sending email...")
    send_email(summary, whoop_data)
    
    print("Clearing notes...")
    clear_notes()
    
    print("Done!")

# ─── Scheduler ───────────────────────────────────────

def run_scheduler():
    schedule.every().day.at("10:00").do(daily_job)
    print("Scheduler running... will send email at 10:00 AM daily")
    while True:
        schedule.run_pending()
        time.sleep(60)

# ─── Main ────────────────────────────────────────────

if __name__ == "__main__":
    if not os.path.exists(TOKENS_FILE):
        print("No tokens found. Starting authentication...")
        webbrowser.open(get_auth_url())
        app.run(port=5000)
    else:
        print("Tokens found! Starting scheduler...")
        run_scheduler()