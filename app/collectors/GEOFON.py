#requierd liberaries
import requests
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
import csv

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

#get the information
site = requests.get(url).text

#parsing html data
soup = BeautifulSoup(site,"html.parser")

#creating csv file and specfying the column of the table
csv_file = open("JAPAN_GEOFON.csv",'w')
csv_witer = csv.writer(csv_file)
csv_witer.writerow(["id","magnitude","depth","time","place","latitude","longitude"])

#lst of all the cards 
list_of_cards = soup.find('div',class_="container-fluid eqlist")

#looping though the cards for acceccing to the data that we needed 
for id,a in enumerate(list_of_cards.find_all('a')):

    #Skip non-earthquake links that don't contain magnitude information.
    try: 
        magnitude = a.find('span',class_="magbox").text

    except AttributeError:
        continue

    #Some earthquake cards use a nested span for depth information.
    #If it doesn't exist, fall back to the text node.
    try: 
        a.find('span',class_="pull-right").find('span')["title"]
        depth = a.find('span',class_="pull-right").find('span').text.replace("*", "")

    except KeyError:
        depth = a.find('span',class_="pull-right").contents[0]

    time = a.find_all('div',class_="col-xs-12")[1].contents[0]
    place = a.strong.text
    Epicenter = a.find('div',class_="col-xs-12")["title"]
    latitude = Epicenter.split(",")[0]
    longitude = Epicenter.split(",")[1]

    #here we saving all the data that we need
    csv_witer.writerow([id,magnitude,depth,time,place,latitude,longitude])

#and never ever forget to close opening file
csv_file.close()