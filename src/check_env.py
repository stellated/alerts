import os
from dotenv import load_dotenv

load_dotenv()

email_alerts_address = os.environ.get("EMAIL_ALERTS_ADDRESS")
sms_phone_number = os.environ.get("SMS_PHONE_NUMBER")
trades_base_folder_mac = os.environ.get("TRADES_BASE_FOLDER_MAC")
trades_base_folder_vm = os.environ.get("TRADES_BASE_FOLDER_VM")
eodhd_api_token = os.environ.get("EODHD_API_TOKEN")
smtp_server = os.environ.get("SMTP_SERVER")
smtp_username = os.environ.get("SMTP_USERNAME")
smtp_password = os.environ.get("SMTP_PASSWORD")
smtp_port = os.environ.get("SMTP_PORT")
clicksend_api_key = os.environ.get("CLICKSEND_API_KEY")
clicksend_username = os.environ.get("CLICKSEND_USERNAME")

print(email_alerts_address)
print(sms_phone_number)
print(trades_base_folder_mac)
print(trades_base_folder_vm)
print(eodhd_api_token)
print(smtp_server)
print(smtp_username)
print(smtp_password)
print(smtp_port)
print(clicksend_api_key)
print(clicksend_username)