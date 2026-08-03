import  matplotlib.pyplot as plt
from sqlalchemy import Select,func
from app.database.models import Earthquake
from app.database.db_manager import managedb
from pprint import pprint
from haversine import haversine
import numpy as np
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker

def histogram_chart():
    stmt = Select(Earthquake.source).group_by(Earthquake.source)
    sources = managedb.read(stmt, "all")

    plt.figure(figsize=(10, 6))

    colors = {
        "GEOFON": "green",
        "MESSY": "lime",
        "EMSC": "blue",
        "USGS": "red"
    }
    for source in sources:
        stmt = Select(Earthquake.magnitude).where(
            Earthquake.source == source
        )

        magnitudes = managedb.read(stmt, "all")
        plt.hist(
            magnitudes,
            bins=15,
            alpha=0.6,
            label=source,
            color=colors[source],
            edgecolor="black"
        )

    plt.xlabel("Magnitude")
    plt.ylabel("Count")
    plt.title("Magnitude Distribution by Source")
    plt.legend()
    plt.grid(axis="y")

    plt.show()

def linear_chart():

    stmt = Select(func.date(Earthquake.time)).group_by(func.date(Earthquake.time)).order_by(func.date(Earthquake.time).asc())
    days = managedb.read(stmt,"all")

    mag_avg = [] 
    for day in days:
        stmt = Select(func.avg(Earthquake.magnitude)).where(func.date(Earthquake.time) == day)
        avg_mag_in_day = managedb.read(stmt,"all")
        mag_avg += avg_mag_in_day

    plt.plot(days,mag_avg,)
    plt.xlabel("days")
    plt.ylabel("avg")
    plt.title("Earthquake Occurrence Trends and Magnitude Variation Over Time")
    plt.show()

def scattter_depth_chart():

    stmt = Select(Earthquake.depth,Earthquake.magnitude)
    earhtquakes = managedb.read(stmt,"all_row")
    depths = [row[0] for row in earhtquakes]
    mags = [row[1] for row in earhtquakes]


    plt.scatter(depths, mags)
    plt.xlabel("Depth")
    plt.ylabel("Magnitude")
    plt.title("Earthquake magnitude and depth")
    plt.show()

    


def blox_plot_chart():
    stmt = Select(Earthquake.depth,Earthquake.magnitude)
    earhtquakes = managedb.read(stmt,"all_row")
    depths = [row[0] for row in earhtquakes]
    mags = [row[1] for row in earhtquakes]

    plt.boxplot(
    [mags, depths],
    label=["magnitude","depths"]
    )
    plt.title("Comparison of earthquake magnitude and depth distributions")
    plt.show()



def heat_map_chart():

    stmt = Select(Earthquake.latitude,Earthquake.longitude)
    earhtquakes = managedb.read(stmt,"all_row")
    latitudes= [row[0] for row in earhtquakes]
    longitudes = [row[1] for row in earhtquakes]

    plt.hexbin(
    longitudes,
    latitudes,
    cmap="coolwarm",
    norm=LogNorm(),
    gridsize=30
    )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.colorbar(label="Earthquake count")
    ax = plt.gca()
    ax.set_facecolor("#1e1e1e")  
    plt.gca().xaxis.set_major_locator(
    ticker.MaxNLocator(8)
    )
    plt.title("Earthquake Geographical Distribution Heatmap")
    plt.show()

def distance_of_tokyo():
    tok_long_lat = (35.6762, 139.6503)

    datas = []
    lat = []
    lon = []
    stmt = Select(Earthquake.latitude,Earthquake.longitude)
    earhtquakes = managedb.read(stmt,"all_row")
    for earthquake in earhtquakes:

        latitudes= earthquake[0]
        longitudes = earthquake[1]
        earth_lat_long = (float(latitudes),float(longitudes))
        distance = haversine(tok_long_lat,earth_lat_long)
        lat.append(latitudes)
        lon.append(longitudes)
        datas.append(distance)

    plt.hexbin(
        lon,
        lat,
        C=datas,
        reduce_C_function=np.mean,
        gridsize=30,
    )

    # plt.hist(distance, bins=20)
    plt.xlabel("Distance from Tokyo (km)")
    plt.ylabel("Earthquake count")
    plt.gca().xaxis.set_major_locator(
    ticker.MaxNLocator(8)
    )
    plt.title("Distance of earthquakes from Tokyo")
    plt.show()



def main():
    histogram_chart()
    linear_chart()
    scattter_depth_chart()
    blox_plot_chart()
    heat_map_chart()
    distance_of_tokyo()

if __name__ == "__main__":
    main()