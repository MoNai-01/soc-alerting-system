import smtplib
import time
from email.mime.text import MIMEText
from pathlib import Path
import hashlib

import os
from dotenv import load_dotenv

load_dotenv("/opt/.env")

# === CONFIGURATION ===
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
ALERT_FILE = "/tmp/security_alerts.txt"
HISTORY_FILE = "/opt/sent_alerts.log"

# Alert type and their subject lines
ALERT_TYPES = {
    "ssh": {
        "subject": "🚨 SSH Brute Force Attempt",
        "match": lambda line: "ssh alert" in line.lower()
    },
    "sqli": {
        "subject": "🚨 SQL Injection Attempt",
        "match": lambda line: "sqli_attempt" in line.lower()
    },
    "xss": {
        "subject": "🚨 XSS Attempt",
        "match": lambda line: "xss_attempt" in line.lower()
    }
}

def hash_line(line):
    return hashlib.sha256(line.strip().encode()).hexdigest()

def load_history():
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, "r") as f:
            return set(line.strip() for line in f)
    return set()

def save_history(sent_hashes):
    with open(HISTORY_FILE, "w") as f:
        for h in sent_hashes:
            f.write(h + "\n")

def determine_alert_type(line):
    for alert_type, config in ALERT_TYPES.items():
        if config["match"](line):
            return alert_type
    return None  # ← don't send generic alerts anymore

def send_email_alert(alert_text, alert_type):
    subject = ALERT_TYPES[alert_type]["subject"]
    msg = MIMEText(alert_text)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Email sent ({alert_type}): {alert_text}")
    except Exception as e:
        print(f"Error sending email: {e}")

def process_alerts():
    if not Path(ALERT_FILE).exists():
        print("Alert file does not exist. Waiting...")
        return

    sent_hashes = load_history()
    new_hashes = set()

    with open(ALERT_FILE, "r") as f:
        for line in f:
            h = hash_line(line)
            if h not in sent_hashes:
                alert_type = determine_alert_type(line)
                if alert_type:  # Only send email if a known alert type
                    send_email_alert(line.strip(), alert_type)
                    new_hashes.add(h)

    save_history(sent_hashes.union(new_hashes))

if __name__ == "__main__":
    print("Monitoring security alerts (SSH, XSS, SQLi)...")
    while True:
        try:
            process_alerts()
            time.sleep(10)
        except KeyboardInterrupt:
            print("\nStopped by user.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

