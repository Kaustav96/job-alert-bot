import smtplib
from email.mime.text import MIMEText

def send_email(subject, html):
    sender = "youroutlook@outlook.com"
    password = "OUTLOOK_APP_PASSWORD"
    receiver = "himasreedam@gmail.com"

    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)