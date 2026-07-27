import requests
from bs4 import BeautifulSoup
from datetime import datetime , timedelta

end_date = datetime.today().date()
start_date = end_date - timedelta(days=30)


url = (f"https://geofon.gfz.de/eqinfo/list.php?datemin={start_date}&datemax=&latmax=46&lonmin=123&lonmax=146&latmin=24&magmin=&fmt=html&nmax=1000")

site = requests.get(url).text

soup = BeautifulSoup(site,"html.parser")

list_of_cards = soup.find('div',class_="container-fluid eqlist")



for index,card in enumerate(list_of_cards.find_all('div',class_="flex-row row eqinfo-all evnrow"),start=1):
    magnitude = card.find('span',class_="magbox").text

    if card.find('span',class_="pull-right").find('span'):
        depth = card.find('span',class_="pull-right").find('span')
    else:
        depth = card.find('span',class_="pull-right").contents[0]

    time = card.find_all('div',class_="col-xs-12")[1].contents[0]
    place = card.strong.text
    Epicenter = card.find('div',class_="col-xs-12")["title"]
    latitude = Epicenter.split(",")[0]
    longitude = Epicenter.split(",")[1]

    print("--------------------")
    print(index)

    print("magnitude",magnitude.strip())
    print("depth",depth.strip())
    print(time.strip())
    print(place.strip())
    print(Epicenter.strip())
    print(latitude.strip())
    print(longitude.strip())
    print("--------------------")