import requests
from datetime import datetime, timedelta
end_date = datetime.today().date()
start_date = end_date - timedelta(days=30)
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
params = {
    "format": "csv",
    "starttime": str(start_date),
    "endtime": str(end_date),
    "minlatitude": 24,
    "maxlatitude": 46,
    "minlongitude": 123,
    "maxlongitude": 146,
    "minmagnitude": 1
}
response = requests.get(url, params=params)
with open("japan_earthquakes.csv", "w", encoding="utf-8") as f:
    f.write(response.text)