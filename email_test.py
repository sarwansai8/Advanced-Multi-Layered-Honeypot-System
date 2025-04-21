import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get email configuration from .env
sender = os.environ.get('ALERT_EMAIL', 'test@example.com')
receiver = os.environ.get('TO_EMAIL', 'test@example.com')
password = os.environ.get('EMAIL_PASSWORD', '')
smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
smtp_port = int(os.environ.get('SMTP_PORT', 587))
use_tls = os.environ.get('USE_TLS', 'False').lower() == 'true'

message = "Subject: Honeypot Email Test\n\nThis is a test email from your Flask honeypot application."

print(f"Attempting to send email from {sender} to {receiver}")
print(f"Using SMTP server: {smtp_server}:{smtp_port}")
print(f"TLS enabled: {use_tls}")

try:
    server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
    
    # Enable TLS encryption if configured
    if use_tls:
        print("Starting TLS...")
        server.starttls()
    
    # Login if not using localhost
    if smtp_server != 'localhost':
        print(f"Logging in as {sender}...")
        server.login(sender, password)
    
    # Send the email
    print("Sending email...")
    server.sendmail(sender, receiver, message)
    server.quit()
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
