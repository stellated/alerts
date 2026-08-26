import os
from dotenv import load_dotenv

load_dotenv()

email_alerts_address = os.environ.get("EMAIL_ALERTS_ADDRESS")
sms_phone_number = os.environ.get("SMS_PHONE_NUMBER")
trades_base_folder_mac = os.environ.get("TRADES_BASE_FOLDER_MAC")
trades_base_folder_vm = os.environ.get("TRADES_BASE_FOLDER_VM")

print(email_alerts_address)
print(sms_phone_number)
print(trades_base_folder_mac)
print(trades_base_folder_vm)