import os
from dotenv import load_dotenv

load_dotenv()

# EODHD
EODHD_API_TOKEN = os.environ.get("EODHD_API_TOKEN")
EODHD_BASE = "https://eodhd.com/api"

# ClickSend
CLICKSEND_API_USERNAME = os.environ.get("CLICKSEND_API_USERNAME")
CLICKSEND_API_KEY = os.environ.get("CLICKSEND_API_KEY")
SMS_PHONE_NUMBER = os.environ.get("SMS_PHONE_NUMBER")

# Email
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 465))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
EMAIL_ALERTS_ADDRESS = os.environ.get("EMAIL_ALERTS_ADDRESS")

# System
SYSTEM = os.environ.get("SYSTEM", "sirius")  # Default to 'sirius' if not set

# Folders
TRADES_BASE_FOLDER_MAC = os.environ.get("TRADES_BASE_FOLDER_MAC")
TRADES_BASE_FOLDER_VM = os.environ.get("TRADES_BASE_FOLDER_VM")

# Set the correct trades folder based on the system
if SYSTEM == "sirius":
    TRADES_BASE_FOLDER = TRADES_BASE_FOLDER_MAC
elif SYSTEM == "sirius":
    TRADES_BASE_FOLDER = TRADES_BASE_FOLDER_MAC
else:
    raise Exception(f"Unknown system {SYSTEM}")


import os
from dotenv import load_dotenv

load_dotenv()

# EODHD
EODHD_API_TOKEN = os.environ.get("EODHD_API_TOKEN")
EODHD_BASE = "https://eodhd.com/api"

# ClickSend
CLICKSEND_API_USERNAME = os.environ.get("CLICKSEND_API_USERNAME")
CLICKSEND_API_KEY = os.environ.get("CLICKSEND_API_KEY")
SMS_PHONE_NUMBER = os.environ.get("SMS_PHONE_NUMBER")

# Email
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 465))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
EMAIL_ALERTS_ADDRESS = os.environ.get("EMAIL_ALERTS_ADDRESS")

# Folders
TRADES_BASE_FOLDER_VM = os.environ.get("TRADES_BASE_FOLDER_VM")