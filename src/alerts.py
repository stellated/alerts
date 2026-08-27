import pandas as pd
from typing import List, Dict
from eodhd import fetch_eod_data


def check_conditions(data: pd.DataFrame, conditions: List[str]) -> List[str]:
    """Check if any alert conditions are met."""
    triggered = []
    if not data.empty:
        latest = data.iloc[-1]  # Most recent day
        prev = data.iloc[-2] if len(data) > 1 else None

        for condition in conditions:
            # Close below X
            if condition.startswith("alert if close below"):
                value = float(condition.split("below")[1].strip())
                if latest["close"] < value:
                    triggered.append(f"Close below {value}")

            # Close above X
            elif condition.startswith("alert if close above"):
                value = float(condition.split("above")[1].strip())
                if latest["close"] > value:
                    triggered.append(f"Close above {value}")

            # Low below X
            elif condition.startswith("alert if low below"):
                value = float(condition.split("below")[1].strip())
                if latest["low"] < value:
                    triggered.append(f"Low below {value}")

            # High above X
            elif condition.startswith("alert if high above"):
                value = float(condition.split("above")[1].strip())
                if latest["high"] > value:
                    triggered.append(f"High above {value}")

            # Up day
            elif condition == "alert on up day":
                if prev is not None:
                    today_hoc = max(latest["open"], latest["close"])
                    today_loc = min(latest["open"], latest["close"])

                    yesterday_hoc = max(prev["open"], prev["close"])
                    yesterday_loc = min(prev["open"], prev["close"])

                    # Check if yesterday was an inside day
                    if (yesterday_hoc <= max(prev["high"], prev["low"]) and
                        yesterday_loc >= min(prev["high"], prev["low"])):
                        if len(data) > 2:
                            prev_prev = data.iloc[-3]
                            yesterday_hoc = max(prev_prev["open"], prev_prev["close"])
                            yesterday_loc = min(prev_prev["open"], prev_prev["close"])

                    if today_hoc > yesterday_hoc and today_loc > yesterday_loc:
                        triggered.append("Up day")

            # Down day
            elif condition == "alert on down day":
                if prev is not None:
                    today_hoc = max(latest["open"], latest["close"])
                    today_loc = min(latest["open"], latest["close"])

                    yesterday_hoc = max(prev["open"], prev["close"])
                    yesterday_loc = min(prev["open"], prev["close"])

                    # Check if yesterday was an inside day
                    if (yesterday_hoc <= max(prev["high"], prev["low"]) and
                        yesterday_loc >= min(prev["high"], prev["low"])):
                        if len(data) > 2:
                            prev_prev = data.iloc[-3]
                            yesterday_hoc = max(prev_prev["open"], prev_prev["close"])
                            yesterday_loc = min(prev_prev["open"], prev_prev["close"])

                    if today_hoc < yesterday_hoc and today_loc < yesterday_loc:
                        triggered.append("Down day")

    return triggered


# def check_conditions(data: pd.DataFrame, conditions: List[str]) -> List[str]:
#     """Check if any alert conditions are met."""
#     triggered = []
#     if not data.empty:
#         latest = data.iloc[-1]  # Most recent day
#         prev = data.iloc[-2] if len(data) > 1 else None
#
#         for condition in conditions:
#             if condition.startswith("alert if close below"):
#                 value = float(condition.split("below")[1].strip())
#                 if latest["close"] < value:
#                     triggered.append(f"Close below {value}")
#
#             elif condition.startswith("alert if low below"):
#                 value = float(condition.split("below")[1].strip())
#                 if latest["low"] < value:
#                     triggered.append(f"Low below {value}")
#
#             elif condition == "alert on up day":
#                 if prev is not None:
#                     # Calculate HOC and LOC for today and yesterday
#                     today_hoc = max(latest["open"], latest["close"])
#                     today_loc = min(latest["open"], latest["close"])
#
#                     yesterday_hoc = max(prev["open"], prev["close"])
#                     yesterday_loc = min(prev["open"], prev["close"])
#
#                     # Check if yesterday was an inside day
#                     if (yesterday_hoc <= max(prev["high"], prev["low"]) and
#                             yesterday_loc >= min(prev["high"], prev["low"])):
#                         # Use day before yesterday
#                         if len(data) > 2:
#                             prev_prev = data.iloc[-3]
#                             yesterday_hoc = max(prev_prev["open"], prev_prev["close"])
#                             yesterday_loc = min(prev_prev["open"], prev_prev["close"])
#
#                     if today_hoc > yesterday_hoc and today_loc > yesterday_loc:
#                         triggered.append("Up day")
#
#     return triggered


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
            print(code, country, triggered)
            if triggered:
                result = {
                    "code": code,
                    "country": country,
                    "conditions": conditions
                }
                print('\t', result)
                results.append(result)
        except Exception as e:
            print(f"Error fetching data for {code}.{country}: {e}")

    print('results', results)

    return results