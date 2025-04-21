import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get email configuration from .env
sender = os.environ.get('ALERT_EMAIL', 'test@example.com')
receiver = os.environ.get('TO_EMAIL', 'test@example.com')
password = os.environ.get('EMAIL_PASSWORD', '')
smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
smtp_port = int(os.environ.get('SMTP_PORT', 587))

# Create a more structured email
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = "Honeypot Email Test (Alternative Method)"

# Email body
body = "This is a test email from your Flask honeypot application using the alternative method."
msg.attach(MIMEText(body, 'plain'))

print(f"Attempting to send email from {sender} to {receiver}")
print(f"Using SMTP server: {smtp_server}:{smtp_port}")

try:
    # Set a shorter timeout (5 seconds instead of 10)
    server = smtplib.SMTP(smtp_server, smtp_port, timeout=5)
    server.ehlo()  # Identify ourselves to the server
    
    # Enable TLS encryption
    print("Starting TLS...")
    server.starttls()
    server.ehlo()  # Re-identify ourselves over TLS connection
    
    # Login
    print(f"Logging in as {sender}...")
    server.login(sender, password)
    
    # Send the email
    print("Sending email...")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
    print("\nTroubleshooting tips:")
    print("1. Check if your network allows outgoing connections on port 587")
    print("2. Verify your Gmail App Password is correct and recently generated")
    print("3. Ensure 2-Factor Authentication is enabled on your Gmail account")
    print("4. Try using a different network connection")
