from email_gmail import send_email

html = """
<h2>Test Email Successful ✅</h2>
<p>This confirms that Gmail App Password and SMTP are working correctly.</p>
"""

send_email("Test Email – Job Alert Bot", html)
print("Email sent successfully!")