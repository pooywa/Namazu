import requests
from datetime import datetime, timedelta
from pathlib import Path

# Store the downloaded CSV next to this script.
CSV_FILE_PATH = Path(__file__).with_name("japan_earthquakes.csv")

# Fetch earthquake data from the last 30 days.
end_date = datetime.today().date()
start_date = end_date - timedelta(days=30)

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

params = {
    "format": "csv",
    "starttime": start_date.isoformat(),
    "endtime": end_date.isoformat(),
    "minlatitude": 24,
    "maxlatitude": 46,
    "minlongitude": 123,
    "maxlongitude": 146,
    "minmagnitude": 1,
}

try:
    # Request earthquake data from the USGS API.
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    # Save the API response as a CSV file.
    CSV_FILE_PATH.write_text(response.text, encoding="utf-8")
    print("Earthquake data saved successfully.")

except requests.exceptions.RequestException as e:
    print(f"USGS request failed: {e}")

# Verify that the file was created successfully before reading it.
if CSV_FILE_PATH.exists():
    try:
        content = CSV_FILE_PATH.read_text(encoding="utf-8")
        print("File read successfully. Length:", len(content))

    except Exception as e:
        print(f"Error reading file: {e}")
else:
    print(
        f"Warning: CSV file does not exist at {CSV_FILE_PATH}. "
        "Please check your network connection and try again."
    )