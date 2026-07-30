import csv
import io
from datetime import datetime, timedelta
from pathlib import Path

import requests

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
OUTPUT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
    / "usgs-earthquakes.csv"
)

CSV_COLUMNS = [
    "DateTime",
    "Latitude",
    "Longitude",
    "Depth(km)",
    "Magnitude",
    "Region",
    "Notes"
]


def get_last_30_days():
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)
    return start_date.isoformat(), end_date.isoformat()


def fetch_earthquakes():
    start_date, end_date = get_last_30_days()
    params = {
        "format": "csv",
        "starttime": start_date,
        "endtime": end_date,
        "minlatitude": 24,
        "maxlatitude": 46,
        "minlongitude": 123,
        "maxlongitude": 146,
        "minmagnitude": 1,
    }

    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    return response.text


def parse_earthquakes(csv_text):
    earthquakes = []

    for row in csv.DictReader(io.StringIO(csv_text)):
        earthquake = {
            "DateTime": row.get("time", "").strip(),
            "Latitude": row.get("latitude", "").strip(),
            "Longitude": row.get("longitude", "").strip(),
            "Depth(km)": row.get("depth", "").strip(),
            "Magnitude": row.get("mag", "").strip(),
            "Region": row.get("place", "").strip(),
        }

        if all(earthquake.values()):
            earthquakes.append(earthquake)

    return earthquakes


def save_to_csv(earthquakes):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(earthquakes)


def main():
    try:
        csv_text = fetch_earthquakes()
        earthquakes = parse_earthquakes(csv_text)

        if not earthquakes:
            print("USGS returned no earthquakes; CSV was not overwritten")
            return

        save_to_csv(earthquakes)
        print(f"Saved {len(earthquakes)} earthquakes to:")
        print(OUTPUT_FILE)

    except requests.RequestException as error:
        print(f"USGS request failed: {error}")
    except OSError as error:
        print(f"Failed to save USGS data: {error}")


if __name__ == "__main__":
    main()
