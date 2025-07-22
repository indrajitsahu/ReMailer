# config.py

from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Database config
DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DRIVER = '{ODBC Driver 18 for SQL Server}'
# DB_ENCRYPT = 'yes'
# DB_TRUST_CERT = 'no'
# DB_TIMEOUT = 30

# Email config (optional for later)
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
FROM_EMAIL = EMAIL_USERNAME

API_KEY = os.getenv('API_KEY')
