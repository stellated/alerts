while testing on PyCharm I think option 2 is most accessible (I've already marked /src as a sources root in PyCharm's IDE.  But deployment onto the environment created by Ubuntu's crontab may not have the same affordances



1:57pm



You're absolutely right. For **PyCharm testing**, **Option 2 (absolute imports)** is more accessible, especially since you’ve already marked `/src` as a **sources root**. However, for **deployment on Ubuntu via cron**, we need a solution that works in both environments without relying on IDE-specific configurations.

------

### **Hybrid Solution: Use Absolute Imports + `PYTHONPATH`**

To ensure the code works **both in PyCharm and on Ubuntu via cron**, we can:

1. **Use absolute imports** in the code (no `.` prefix).
2. **Set the `PYTHONPATH`** in the cron environment to include the project root.

------

### **Step 1: Update Imports in All Files**

Replace all **relative imports** (e.g., `from .config import ...`) with **absolute imports** (e.g., `from config import ...`).

#### **Example Updates**

1. **`main.py`**:

   python

   Copy

   ```
   from config import TRADES_BASE_FOLDER_VM
   from parser import get_trade_files
   from alerts import check_all_alerts
   from notifier import notify_alerts
   ```

2. **`alerts.py`**:

   python

   Copy

   ```
   from eodhd import fetch_eod_data
   ```

3. **`notifier.py`**:

   python

   Copy

   ```
   from config import (
       SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD,
       EMAIL_ALERTS_ADDRESS, CLICKSEND_API_USERNAME,
       CLICKSEND_API_KEY, SMS_PHONE_NUMBER
   )
   ```

4. **`parser.py`**:
   No changes needed (no relative imports).

5. **`eodhd.py`**:

   python

   Copy

   ```
   from config import EODHD_API_TOKEN, EODHD_BASE
   ```

------

### **Step 2: Set `PYTHONPATH` in Cron**

In your **cron job**, set the `PYTHONPATH` to include the project root (`/path/to/alerts/`). This ensures Python can resolve the absolute imports.

#### **Cron Entry**

bash

Copy

```
# Run every hour at minute 30
30 * * * * PYTHONPATH=/path/to/alerts /usr/bin/python3 /path/to/alerts/src/main.py
```

Replace `/path/to/alerts/` with the actual path to your project on the Ubuntu VM.

------

### **Step 3: Test in PyCharm**

Since you’ve marked `/src` as a **sources root** in PyCharm, the absolute imports will work automatically in the IDE. No further changes are needed.

------

### **Step 4: Test on Ubuntu**

1. **Manually test** the script with `PYTHONPATH` set:

   bash

   Copy

   ```
   PYTHONPATH=/path/to/alerts /usr/bin/python3 /path/to/alerts/src/main.py
   ```

   This simulates the cron environment.

2. **Verify cron**:

   - Add the cron job as shown above.

   - Check logs for errors:

     bash

     Copy

     ```
     grep CRON /var/log/syslog
     ```

------

### **Why This Works**

- **PyCharm**: Recognizes `/src` as a sources root, so absolute imports resolve correctly.
- **Cron**: `PYTHONPATH` ensures Python can find the `src` directory and resolve the imports.