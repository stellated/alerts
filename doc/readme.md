### End of day stock price alerts

#### About me

I am Australian, I live in Melbourne.  My name is Ian.

I have a subscription to eodhd for stock market data.

I trade USA and Australian stocks.  The possibility of trading other countries' markets does exist, but is out of scope for now.

I like my code in python and my data in an sqlite database.

I have a Macintosh laptop and a virtual machine with Ubuntu Linux provided by Digital Ocean.  I connect to it by ssh, with ssh handling passwords via config set up in ~/.ssh .  

I subscribe to a stock tipping service and I track tips and trades in markdown files.  File naming is:

* yyww.code.country.n.status.md
* yy = year
* ww = week of year
* code = 'BSL' for Bluescope Steel, for example
* country = 'AX' for Australia, 'US' for USA
* n = the nth file associated with this trade
* status = 'watch', 'open', etc



#### What I want

I want a python script, running on my VM, to alert me by email and sms when a stock triggers a condition listed in its markdown file.

For now, the script will work at the end of each day.  Intraday alerts are out of scope.

I will put Instructions for the script into my markdown notes, each such line starts with ">" .  Sample markdown files are included.

Since I create my markdown files on the Mac, there will also need to be a synchronisation between the folder where they live and a folder on the VM.  Perhaps an rsync script that runs on the mac upon machine startup and every 10 minutes.  So that's a second project within the main project.

Only markdown files in the base folder of my trading notes and with status of "watch" or "open" are to be scanned.  The stock code, and country, are to be inferred from the file names.  If there are multiple files for the same trade, take the one with the highest n. 



#### Alert syntax

Instructions like "alert if close below 30.50" or "alert if low below 30.00" are obvious. 

"Alert on up day" - in candlestick charting terms, alert if the ends of the body of today's candle are both above the corresponding ends of yesterday's candle.  That is, if today's HOC > yesterday's HOC and today's LOC > yesterday's LOC, where HOC = higher of open and close and LOC = lower of open and close.  Furthermore, if yesterday was an inside day then take the HOC and LOC from the day before yesterday.



#### Environment variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

email_alerts_address = os.environ.get("EMAIL_ALERST_ADDRESS")
sms_phone_number = os.environ.get("SMS_PHONE_NUMBER")
trades_base_folder_mac = os.environ.get("TRADES_BASE_FOLDER_MAC")
trades_base_folder_vm = os.environ.get("TRADES_BASE_FOLDER_VM")

```

Let me know if there's anything else I need to set up.



#### Test environment

I will test code on my laptop for an extended period.  Deployment to the VM will only happen when I'm confident the code is ready.

Code is on GitHub at git@github.com:stellated/alerts.git


#### Two VMs

The VM on which this code was deployed is being ended soon
Introduction to Claude Code CLI will occur on the new VM (mars)


#### Time of Day of Execution

The crontab entry on the old VM is/was
30 * * * 1-5 PYTHONPATH=/home/ian/repos/alerts/src /home/ian/repos/alerts/.venv/bin/python /home/ian/repos/alerts/src/main.py > /home/ian/repos/alerts/main.out.txt 2>&1

The code is being run hourly at half past the hour.  
Execution of the task happens when the code detects that the time in Australia is 4:30 pm
Thus the code is able to perform its function while hosted on a VM with a non-Australian system clock.



