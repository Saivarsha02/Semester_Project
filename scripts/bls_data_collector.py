import requests
import pandas as pd
import json
from datetime import datetime

# Constants
API_KEY = "09298fcd9b9e437782ed966abc0e6d43"  # Replace with your BLS API key
SERIES_IDS = ['CES0000000001', 'CES0500000001', 'CES2000000001', 'CES3000000001',
              'CES4000000001', 'CES6000000001', 'CES7000000001', 'CES8000000001',
              'LNS14000000', 'LNS11300000', 'LNS12300000', 'LNS13023621',
              'LNS12032194', 'LNS12500000', 'LNS12600000']
# Non-farm workers, unemployment rate, and more
START_YEAR = "2000"
END_YEAR = str(datetime.now().year)

# Mapping series IDs to descriptive names
SERIES_ID_NAME_MAP = {
    "CES0000000001": "Total Nonfarm Employment",
    "CES0500000001": "Total Private Employment",
    "CES2000000001": "Construction Employment",
    "CES3000000001": "Manufacturing Employment",
    "CES4000000001": "Trade, Transportation, and Utilities Employment",
    "CES6000000001": "Professional and Business Services Employment",
    "CES7000000001": "Education and Health Services Employment",
    "CES8000000001": "Leisure and Hospitality Employment",
    "LNS14000000": "Unemployment Rate",
    "LNS11300000": "Labor Force Participation Rate",
    "LNS12300000": "Civilian Employment-Population Ratio",
    "LNS13023621": "Part-Time for Economic Reasons",
    "LNS12032194": "Women Labor Force Participation",
    "LNS12500000": "Median Duration of Unemployment",
    "LNS12600000": "Average Hourly Earnings"
}

def fetch_bls_data(series_ids, start_year, end_year, api_key):
    """Fetch data from BLS API."""
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "seriesid": series_ids,
        "startyear": start_year,
        "endyear": end_year,
        "registrationkey": api_key
    })
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        raise ValueError("Error fetching data from BLS API.")
    return response.json()["Results"]["series"]

def process_bls_data(data):
    """Process raw data into a DataFrame."""
    records = []
    for series in data:
        series_id = series["seriesID"]
        for entry in series["data"]:
            records.append({
                "series_id": series_id,
                "year": int(entry["year"]),
                "period": entry["period"],
                "period_name": entry["periodName"],
                "value": float(entry["value"]),
            })
    return pd.DataFrame(records)

if __name__ == "__main__":
    data = fetch_bls_data(SERIES_IDS, START_YEAR, END_YEAR, API_KEY)
    df = process_bls_data(data)
    df.to_csv("data/labor_stats.csv", index=False) #storing the collected data in labor_stats named file 
    print("Data collection complete.")
