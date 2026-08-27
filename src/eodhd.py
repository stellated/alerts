import requests
import pandas as pd
from .config import EODHD_API_TOKEN, EODHD_BASE

def fetch_eod_data(code: str, country: str) -> pd.DataFrame:
    """Fetch end-of-day data for a stock from EODHD."""
    params = {
        "api_token": EODHD_API_TOKEN,
        "fmt": "json",
        "period": "d"
    }
    url = f"{EODHD_BASE}/eod/{code}.{country}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data)