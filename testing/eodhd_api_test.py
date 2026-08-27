from src.eodhd import fetch_eod_data

data = fetch_eod_data("BSL", "AU")
print(data.head())