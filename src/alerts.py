import pandas as pd
from typing import List, Dict
from .eodhd import fetch_eod_data


def check_conditions(data: pd.DataFrame, conditions: List[str]) -> List[str]:
    """Check if any alert conditions are met."""
    triggered = []
    if not data.empty:
        latest = data.iloc[-1]  # Most recent day
        prev = data.iloc[-2] if len(data) > 1 else None

        for condition in conditions:
            if condition.startswith("alert if close below"):
                value = float(condition.split("below")[1].strip())
                if latest["Close"] < value:
                    triggered.append(f"Close below {value}")

            elif condition.startswith("alert if low below"):
                value = float(condition.split("below")[1].strip())
                if latest["Low"] < value:
                    triggered.append(f"Low below {value}")

            elif condition == "alert on up day":
                if prev is not None:
                    # Calculate HOC and LOC for today and yesterday
                    today_hoc = max(latest["Open"], latest["Close"])
                    today_loc = min(latest["Open"], latest["Close"])

                    yesterday_hoc = max(prev["Open"], prev["Close"])
                    yesterday_loc = min(prev["Open"], prev["Close"])

                    # Check if yesterday was an inside day
                    if (yesterday_hoc <= max(prev["High"], prev["Low"]) and
                            yesterday_loc >= min(prev["High"], prev["Low"])):
                        # Use day before yesterday
                        if len(data) > 2:
                            prev_prev = data.iloc[-3]
                            yesterday_hoc = max(prev_prev["Open"], prev_prev["Close"])
                            yesterday_loc = min(prev_prev["Open"], prev_prev["Close"])

                    if today_hoc > yesterday_hoc and today_loc > yesterday_loc:
                        triggered.append("Up day")

    return triggered


def check_all_alerts(trade_files: List[Dict]) -> List[Dict]:
    """Check all trade files for triggered alerts."""
    results = []
    for trade in trade_files:
        code = trade["code"]
        country = trade["country"]
        conditions = trade["conditions"]

        try:
            data = fetch_eod_data(code, country)
            triggered = check_conditions(data, conditions)
            if triggered:
                results.append({
                    "code": code,
                    "country": country,
                    "conditions": triggered
                })
        except Exception as e:
            print(f"Error fetching data for {code}.{country}: {e}")

    return results