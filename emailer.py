import smtplib
import os
from dotenv import load_dotenv
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlparse
from datetime import datetime

load_dotenv()



EMAIL = os.getenv("EMAIL_ADDRESS")
PWD = os.getenv("EMAIL_PASSWORD")
HOST = os.getenv("EMAIL_HOST")
PORT = int(os.getenv("EMAIL_PORT"))

print(EMAIL)

TO_EMAIL = "samohthung@gmail.com"


def build_body(articles):
   
    lines = []

    for item in articles:
       title = item["title"]
       date = item["date"]
       if isinstance(date, datetime):
            date = date.strftime("%b %d, %Y %I:%M %p %Z")
       URL = item["url"]
       body = item["content"]

       lines.append(
           f"{title} – {date}\n{URL}\n{body}\n" + "="*60 + "\n"
       )
    
    return "EM News Digest\n\n" + "\n".join(lines)

def send_email(content):
    subject = "Test Email from EM News Bot"

    # Build a proper MIMEText with utf-8
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    try:
        with smtplib.SMTP(HOST, PORT) as server:
            server.starttls()
            server.login(EMAIL, PWD)
            server.send_message(msg)              # <-- correct: send MIME object
            # alternatively: server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
        print(f"Email sent successfully to {TO_EMAIL}")
    except Exception as e:
        print("Error:", e)