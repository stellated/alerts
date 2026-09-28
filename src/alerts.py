import pandas as pd
from typing import List, Dict, Tuple
from eodhd import fetch_eod_data


def body_ends(candle: pd.Series) -> Tuple[float, float]:
    """Return (HOC, LOC): the higher and lower of open and close."""
    return max(candle["open"], candle["close"]), min(candle["open"], candle["close"])


def is_inside_day(day: pd.Series, prior: pd.Series) -> bool:
    """True if day's body (HOC/LOC) lies within prior's body. Equal values count as inside."""
    day_hoc, day_loc = body_ends(day)
    prior_hoc, prior_loc = body_ends(prior)
    return day_hoc <= prior_hoc and day_loc >= prior_loc


def reference_candle(data: pd.DataFrame) -> pd.Series:
    """Candle that today is compared against for up/down day.

    Yesterday, unless yesterday was an inside day, in which case the day before yesterday.
    Only steps back once, even if the day before yesterday was also an inside day.
    """
    prev = data.iloc[-2]
    if len(data) > 2 and is_inside_day(prev, data.iloc[-3]):
        return data.iloc[-3]
    return prev


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

            # Up day / down day
            elif condition in ("alert on up day", "alert on down day"):
                if prev is not None:
                    today_hoc, today_loc = body_ends(latest)
                    ref_hoc, ref_loc = body_ends(reference_candle(data))
                    if condition == "alert on up day":
                        if today_hoc > ref_hoc and today_loc > ref_loc:
                            triggered.append("Up day")
                    else:
                        if today_hoc < ref_hoc and today_loc < ref_loc:
                            triggered.append("Down day")

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
            print(code, country, triggered)
            if triggered:
                result = {
                    "code": code,
                    "country": country,
                    "triggered": triggered
                }
                print('\t', result)
                results.append(result)
        except Exception as e:
            print(f"Error fetching data for {code}.{country}: {e}")

    print(f"{len(results)} results:")
    for result in results:
        print('\t', result)

    return results