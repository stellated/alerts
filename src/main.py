from datetime import datetime
import pytz
from .config import TRADES_BASE_FOLDER_VM
from .parser import get_trade_files
from .alerts import check_all_alerts
from .notifier import notify_alerts


def main():
    # Time zone check: Run only at 4:30 PM Melbourne time
    melb_tz = pytz.timezone("Australia/Melbourne")
    current_melb_time = datetime.now(melb_tz).time()

    if current_melb_time.hour != 16 or current_melb_time.minute != 30:
        print(f"Not 4:30 PM Melbourne time. Current time: {current_melb_time}")
        return

    print("Running stock alerts at 4:30 PM Melbourne time...")

    # Get trade files
    trade_files = get_trade_files(TRADES_BASE_FOLDER_VM)
    print(f"Found {len(trade_files)} trade files to monitor.")

    # Check alerts
    alerts = check_all_alerts(trade_files)
    print(f"Triggered {len(alerts)} alerts.")

    # Notify
    if alerts:
        notify_alerts(alerts)
        print("Notifications sent.")
    else:
        print("No alerts triggered.")


if __name__ == "__main__":
    main()