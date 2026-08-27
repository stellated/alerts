## File Structure

```
alerts/
├── src/
│   ├── __init__.py
│   ├── config.py          # Load environment variables
│   ├── eodhd.py           # Fetch EOD data from EODHD API
│   ├── parser.py          # Parse markdown trade notes
│   ├── alerts.py          # Check alert conditions
│   ├── notifier.py        # Send email/SMS notifications
│   └── main.py            # Main script logic
├── trades/                # Markdown trade notes
├── .env                   # Environment variables
└── requirements.txt       # Python dependencies
```

## Environment Variables

```bash
# EODHD API
EODHD_API_TOKEN=your_eodhd_api_token

# ClickSend SMS
CLICKSEND_API_USERNAME=your_clicksend_username
CLICKSEND_API_KEY=your_clicksend_api_key
SMS_PHONE_NUMBER=+614XXXXXXXX

# Email (VentraIP)
SMTP_SERVER=mail.ventraip.com.au
SMTP_PORT=465
SMTP_USERNAME=your_email@domain.com
SMTP_PASSWORD=your_email_password
EMAIL_ALERTS_ADDRESS=your_email@domain.com

# Folders
TRADES_BASE_FOLDER_MAC=/path/on/mac
TRADES_BASE_FOLDER_VM=/path/on/vm
```

## Cron Setup

Add this to your VM's crontab (`crontab -e`):

```bash
# Run every hour at minute 30
30 * * * * /usr/bin/python3 /path/to/alerts/src/main.py
```

------

## Requirements

```bash
python-dotenv==1.0.0
pandas==2.0.3
requests==2.31.0
pytz==2023.3
```

## Testing

1. **Test EODHD API**:

   ```python
    from src.eodhd import fetch_eod_data
    data = fetch_eod_data("BSL", "AX")
    print(data.head())
   ```

2. **Test Parser**:

   ```python
    from src.parser import get_trade_files
    files = get_trade_files("/path/to/trades")
    print(files)
   ```

3. **Test Alerts**:

   ```python
    from src.alerts import check_all_alerts
    alerts = check_all_alerts([{"code": "BSL", "country": "AX", "conditions": ["alert if close below 30.50"]}])
    print(alerts)
   ```

4. **Test Notifications**:

   ```python
    from src.notifier import send_email, send_sms
    send_email("Test Subject", "Test Body")
    send_sms("Test SMS")
   ```

## Deployment

1. **Sync Files**: Use `rsync` to sync `/trades/` from Mac to VM.
    Example cron on Mac:

   ```bash
    */10 * * * * rsync -avz /path/on/mac/ user@vm:/path/on/vm/
   ```

2. **Run on VM**: Ensure Python and dependencies are installed on the VM.

3. **Monitor Logs**: Check cron logs for errors:

   ```bash
    grep CRON /var/log/syslog
   ```