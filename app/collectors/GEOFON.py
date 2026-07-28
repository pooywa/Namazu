#requierd liberaries
import requests
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
from app.utils.save_to_file_csv import save_csv

#Date range: last 30 days
end_date = datetime.today().date()
start_date = end_date - timedelta(days=30)

#config data for the url
latmax = "46"
lonmin = "123" 
lonmax = "146"
latmin = "24"
nmax = "1000" 

#customizing our url with desired config
url = (f"https://geofon.gfz.de/eqinfo/list.php?datemin={start_date}&datemax={end_date}&latmax={latmax}&lonmin={lonmin}&lonmax={lonmax}&latmin={latmin}&magmin=&fmt=html&nmax={nmax}")

def cleaning(data:str):
    return data.strip()

def fetch_data(url):
    #get site
    site = requests.get(url).text
    return site

def extract_data(a):

    #Skip non-earthquake links that don't contain magnitude information.
    try: 
        magnitude = cleaning(a.find('span',class_="magbox").text)
    except AttributeError:
        return None,None,None,None,None,None

    #If it doesn't exist, fall back to the text node.
    try: 
        a.find('span',class_="pull-right").find('span')["title"]
        depth = cleaning(a.find('span',class_="pull-right").find('span').text.replace("*", ""))

    except KeyError:
        depth = cleaning(a.find('span',class_="pull-right").contents[0])

    time = cleaning(a.find_all('div',class_="col-xs-12")[1].contents[0])
    place = cleaning(a.strong.text)
    Epicenter = cleaning(a.find('div',class_="col-xs-12")["title"])
    longitude = cleaning(Epicenter.split(",")[0])
    latitude = cleaning(Epicenter.split(",")[1])

    return time,longitude,latitude,place,magnitude,depth

def pars_data(page):
    soup = BeautifulSoup(page,"html.parser")

    #storage dict for save csv file
    data = []

    #lst of all the cards 
    list_of_cards = soup.find('div',class_="container-fluid eqlist")

    #looping though the cards for acceccing to the data that we needed 
    for a in list_of_cards.find_all('a'):
        time,longitude,latitude,place,magnitude,depth = extract_data(a)
        if not time:
            continue
        data.append({"DateTime":time,"Latitude":latitude,"Longitude":longitude,"Depth(km)":depth,"Magnitude":magnitude,"Region":place})

    return data

def main():
    page = fetch_data(url)
    data = pars_data(page)
    save_csv("JAPAN_GEOFON.csv",data)

main() 