from datetime import date, timedelta
import requests
import pandas as pd
from config import EODHD_API_TOKEN, EODHD_BASE

# Calendar days of history to fetch: enough for up/down day (3 bars) across long holiday breaks
LOOKBACK_DAYS = 20


def fetch_eod_data(code: str, country: str) -> pd.DataFrame:
    """Fetch recent end-of-day data for a stock from EODHD.

    Raises requests.HTTPError on failure; EODHD returns 404 for an unknown ticker.
    """
    params = {
        "api_token": EODHD_API_TOKEN,
        "fmt": "json",
        "period": "d",
        "from": (date.today() - timedelta(days=LOOKBACK_DAYS)).isoformat(),
    }
    url = f"{EODHD_BASE}/eod/{code}.{country}"
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data)
