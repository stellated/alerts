import smtplib
from email.mime.text import MIMEText
import requests
import base64
from config import (
    SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD,
    EMAIL_ALERTS_ADDRESS, CLICKSEND_API_USERNAME,
    CLICKSEND_API_KEY, SMS_PHONE_NUMBER
)


def send_email(subject: str, body: str) -> None:
    """Send an email alert."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = EMAIL_ALERTS_ADDRESS
    print("Sending email...")

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        status_code, response_text = server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print(f"server.login(), status code (should be 235): {status_code} response text: {response_text}")
        failed_recipients = server.sendmail(SMTP_USERNAME, [EMAIL_ALERTS_ADDRESS], msg.as_string())
        print(f"server.sendmail() failed recipients (should be empty dict): {failed_recipients}")



def send_sms(message: str) -> None:
    """Send an SMS alert via ClickSend."""
    # Encode username:api_key in Base64
    auth_string = f"{CLICKSEND_API_USERNAME}:{CLICKSEND_API_KEY}"
    auth_bytes = auth_string.encode("ascii")
    base64_auth = base64.b64encode(auth_bytes).decode("ascii")

    print("Sending SMS alert...")

    url = "https://api.clicksend.com/v3/sms/send"
    payload = {
        "messages": [
            {
                "to": SMS_PHONE_NUMBER,
                "body": message,
                # Omit 'from' to use a shared number during trial
            }
        ]
    }
    headers = {
        "Authorization": f"Basic {base64_auth}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if not response.ok:
        print("ClickSend error response", response.text)
    response.raise_for_status()


def notify_alerts(alerts: list[dict]) -> None:
    """Send notifications for triggered alerts."""
    if not alerts:
        return

    # Email
    subject = f"{len(alerts)} Stock Alerts Triggered"
    body = "\n".join(
        [f"{alert['code']}({alert['country']}): {', '.join(alert['triggered'])}" for alert in alerts])
    send_email(subject, body)

    # SMS
    sms_message = f"{len(alerts)} Stock Alerts:\n{body}"
    send_sms(sms_message)