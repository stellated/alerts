import re
import pandas as pd
from typing import List, Dict, Optional, Tuple
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


# Price conditions: prefix -> (candle field, test, label)
PRICE_CONDITIONS = {
    "alert if close below": ("close", lambda price, value: price < value, "Close below"),
    "alert if close above": ("close", lambda price, value: price > value, "Close above"),
    "alert if low below": ("low", lambda price, value: price < value, "Low below"),
    "alert if high above": ("high", lambda price, value: price > value, "High above"),
}

# A price such as 30.50 or $30.50, and nothing else
PRICE_PATTERN = re.compile(r"\$?\s*(\d+(?:\.\d+)?)")


def parse_price(text: str) -> Optional[float]:
    """Parse a price like '30.50' or '$30.50'. Returns None if text isn't a plain price."""
    match = PRICE_PATTERN.fullmatch(text.strip())
    return float(match.group(1)) if match else None


def check_conditions(data: pd.DataFrame, conditions: List[str]) -> List[str]:
    """Check if any alert conditions are met.

    Unrecognised conditions and bad prices are reported as ERROR entries so they get notified.
    Matching ignores case, so "Alert on up day" works.
    """
    triggered = []
    if not data.empty:
        latest = data.iloc[-1]  # Most recent day
        prev = data.iloc[-2] if len(data) > 1 else None

        for condition in conditions:
            normalised = condition.lower()
            price_prefix = next((p for p in PRICE_CONDITIONS if normalised.startswith(p)), None)

            # Close/low/high below/above X
            if price_prefix:
                field, test, label = PRICE_CONDITIONS[price_prefix]
                value = parse_price(normalised[len(price_prefix):])
                if value is None:
                    triggered.append(f"ERROR bad price in condition: '{condition}'")
                elif test(latest[field], value):
                    triggered.append(f"{label} {value}")

            # Up day / down day
            elif normalised in ("alert on up day", "alert on down day"):
                if prev is not None:
                    today_hoc, today_loc = body_ends(latest)
                    ref_hoc, ref_loc = body_ends(reference_candle(data))
                    if normalised == "alert on up day":
                        if today_hoc > ref_hoc and today_loc > ref_loc:
                            triggered.append("Up day")
                    else:
                        if today_hoc < ref_hoc and today_loc < ref_loc:
                            triggered.append("Down day")

            # Anything else is a typo or unsupported syntax: report it so it isn't silently ignored
            else:
                triggered.append(f"ERROR unrecognised condition: '{condition}'")

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