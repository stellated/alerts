from src.alerts import check_all_alerts

alerts = check_all_alerts([{"code": "BSL", "country": "AU", "conditions": ["alert if close below 30.50"]}])
print(alerts)