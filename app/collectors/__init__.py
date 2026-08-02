from app.collectors.emsc import main as emcs_main
from app.collectors.GEOFON import main as geofon_main
from app.collectors.USGS import  main as usgs_main


def main():
    emcs_main()
    geofon_main()
    usgs_main()