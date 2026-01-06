import smtplib
import os
from email.mime.text import MIMEText

def send_email(subject, html):
    sender = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASSWORD")
    receiver = "himasreedam@gmail.com"
    # receiver = "1415016@kiit.ac.in"

    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)