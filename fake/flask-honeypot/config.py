import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # Email Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    ALERT_EMAIL = os.getenv('ALERT_EMAIL')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    TO_EMAIL = os.getenv('TO_EMAIL')
    USE_TLS = os.getenv('USE_TLS', 'True').lower() == 'true'

    # IP Info API Configuration
    IPINFO_API_KEY = os.getenv('IPINFO_API_KEY', '')
    
    # Future Add-ons
    # DATABASE_URI = os.getenv('DATABASE_URI')
    # LOG_PATH = os.getenv('LOG_PATH', 'logs.txt')
