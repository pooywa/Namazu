#requierd liberaries
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
from app.utils.save_to_file_csv import save_csv

#Date range: last 30 days
today = datetime.today().date()
end_date = today - timedelta(days=1)
start_date = today - timedelta(days=30)

#config data for the url
latmax = "46"
lonmin = "123" 
lonmax = "146"
latmin = "24"
nmax = "1000" 

#customizing our url with desired config
url = (f"https://geofon.gfz.de/eqinfo/list.php")

PARAMS = {
    "datemin": start_date,
    "datemax": end_date,
    "latmin": latmin,
    "latmax": latmax,
    "lonmin": lonmin,
    "lonmax": lonmax,
    "magmin": "",
    "fmt": "html",
    "nmax": nmax,
}

OUTPUT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
    / "geofon-earthquakes.csv"
)

def cleaning(data:str):
    return data.strip()

def fetch_data(url,params,timeout):
    #get site
    response = requests.get(url=url,params=params, timeout=timeout)
    response.raise_for_status()
    return response.text

def extract_data(a):

    #Skip non-earthquake links that don't contain magnitude information.
    try: 
        magnitude = a.find('span',class_="magbox").get_text("", strip=True)
    except AttributeError:
        return {"error":True,"data": {}}

    try: 
        a.find('span',class_="pull-right").find('span')["title"]
        depth = cleaning(a.find('span',class_="pull-right").find('span').text.replace("*", ""))

    except KeyError:
        depth = cleaning(a.find('span',class_="pull-right").contents[0])

    time = a.find_all('div',class_="col-xs-12")[1].contents[0].get_text("", strip=True)
    place = a.strong.get_text("",strip=True)
    Epicenter = cleaning(a.find('div',class_="col-xs-12")["title"])#.get_text("", strip=True)
    longitude = cleaning(Epicenter.split(",")[0]).replace("°E","")
    latitude = cleaning(Epicenter.split(",")[1]).replace("°N","")

    return {"error": False,"data": {
    "DateTime": time,
    "Latitude": float(latitude),
    "Longitude": float(longitude),
    "Depth(km)": depth,
    "Magnitude": magnitude,
    "Region": place,}
    }

def pars_data(page):
    soup = BeautifulSoup(page,"html.parser")

    #storage dict for save csv file
    data = []

    #lst of all the cards 
    list_of_cards = soup.find('div',class_="container-fluid eqlist")

    if list_of_cards is None:
        raise ValueError("GEOFON earthquake list was not found")

    #looping though the cards for acceccing to the data that we needed 
    for a in list_of_cards.find_all('a'):
        ext_data = extract_data(a)
        if ext_data["error"]:
            continue
        data.append(ext_data["data"])

    return data

def main():
    page = fetch_data(url,params=PARAMS,timeout=30)
    data = pars_data(page)
    save_csv(OUTPUT_FILE,data)


if __name__ == "__main__":
    main()