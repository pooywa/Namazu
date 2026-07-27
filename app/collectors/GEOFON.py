import requests
from bs4 import BeautifulSoup
from datetime import datetime , timedelta
import csv

end_date = datetime.today().date()
start_date = end_date - timedelta(days=30)


url = (f"https://geofon.gfz.de/eqinfo/list.php?datemin={start_date}&datemax=&latmax=46&lonmin=123&lonmax=146&latmin=24&magmin=&fmt=html&nmax=1000")

site = requests.get(url).text

soup = BeautifulSoup(site,"html.parser")

csv_file = open("JAPAN_GEOFON.csv",'w')
csv_witer = csv.writer(csv_file)
csv_witer.writerow(["id","magnitude","depth","time","place","latitude","longitude"])

list_of_cards = soup.find('div',class_="container-fluid eqlist")

for id,a in enumerate(list_of_cards.find_all('a')):

    try: 
        magnitude = a.find('span',class_="magbox").text
    except AttributeError:
        continue

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

    csv_witer.writerow([id,magnitude,depth,time,place,latitude,longitude])

csv_file.close()