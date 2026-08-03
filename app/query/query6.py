from sqlalchemy import select, func
from app.database.db_manager import managedb
from app.database.models import Earthquake
from tabulate import tabulate
from colorama import Fore, Style


def total_record_of_each_source():

    stmt = select(Earthquake.source, func.count("*"))\
           .group_by(Earthquake.source)

    result = managedb.read(stmt, "all_row")
    return result


def avg_mag_record_of_each_source():

    stmt = select(Earthquake.source, func.avg(Earthquake.magnitude))\
           .group_by(Earthquake.source)

    result = managedb.read(stmt, "all_row")
    return result


def avg_depth_record_of_each_source():

    stmt = select(Earthquake.source, func.avg(Earthquake.depth))\
           .group_by(Earthquake.source)

    result = managedb.read(stmt, "all_row")
    return result


def number_of_record_by_area():

    stmt = select(
        Earthquake.place,
        Earthquake.source,
        func.count("*")
    )\
    .group_by(
        Earthquake.place,
        Earthquake.source
    )\
    .order_by(Earthquake.place)

    result = managedb.read(stmt, "all_row")
    return result


def number_of_each_category():

    stmt = select(
        Earthquake.source,
        Earthquake.category,
        func.count("*")
    )\
    .group_by(
        Earthquake.source,
        Earthquake.category
    )\
    .order_by(Earthquake.source)

    result = managedb.read(stmt, "all_row")
    return result


def main():

    print(
        Fore.CYAN +
        Style.BRIGHT +
        "\n=== Total records of each source ===\n" +
        Style.RESET_ALL
    )

    total = total_record_of_each_source()
    print(
        Fore.YELLOW +
        tabulate(
            total,
            ['sources', 'number of sources'],
            tablefmt="heavy_grid"
        ) +
        Style.RESET_ALL
    )


    print(
        Fore.CYAN +
        Style.BRIGHT +
        "\n=== Average magnitude of each source ===\n" +
        Style.RESET_ALL
    )

    avg_mag = avg_mag_record_of_each_source()
    print(
        Fore.GREEN +
        tabulate(
            avg_mag,
            ['sources', 'average magnitude of each sources'],
            tablefmt="heavy_grid"
        ) +
        Style.RESET_ALL
    )


    print(
        Fore.CYAN +
        Style.BRIGHT +
        "\n=== Average depth of each source ===\n" +
        Style.RESET_ALL
    )

    avg_depth = avg_depth_record_of_each_source()
    print(
        Fore.BLUE +
        tabulate(
            avg_depth,
            ['sources', 'average depth of each sources'],
            tablefmt="heavy_grid"
        ) +
        Style.RESET_ALL
    )


    print(
        Fore.CYAN +
        Style.BRIGHT +
        "\n=== Number of records by area ===\n" +
        Style.RESET_ALL
    )

    area = number_of_record_by_area()
    print(
        Fore.MAGENTA +
        tabulate(
            area,
            ['place', 'source', "number of area"],
            tablefmt="heavy_grid"
        ) +
        Style.RESET_ALL
    )


    print(
        Fore.CYAN +
        Style.BRIGHT +
        "\n=== Number of each category ===\n" +
        Style.RESET_ALL
    )

    category = number_of_each_category()
    print(
        Fore.YELLOW +
        tabulate(
            category,
            ['source', 'category', "number of category"],
            tablefmt="heavy_grid"
        ) +
        Style.RESET_ALL
    )


# if __name__ == "__main__":
#     main()
    print(tabulate(category,
                        ['source','category',"number of category"],
                        tablefmt="heavy_grid"))

    print('''\n
    1.EMSC provides the largest number of earthquake records (231), 
    making it the primary data source. 
    USGS contributes a moderate number of events (69), while GEOFON (35) 
    and MESSY (30) provide smaller datasets.''')

    print('''\n
    2.GEOFON reports the highest average earthquake magnitude (4.99), 
    followed closely by MESSY (4.82) and USGS (4.60). 
    EMSC has the lowest average magnitude (3.74), suggesting it captures 
    a larger number of weaker earthquakes.''')

    print('''\n
    3.MESSY reports the deepest earthquakes on average (129.36 km), 
    while GEOFON (86.06 km) and USGS (85.40 km) show similar average depths. 
    EMSC has the shallowest average depth (35.84 km), indicating it mainly 
    records shallow seismic events.''')

    print('''\n
    4.The results show that the same earthquake regions are reported with 
    different naming conventions across data sources. For example, 
    'KYUSHU, JAPAN', 'Kyushu, Japan', and several similar variations refer 
    to the same geographic area. EMSC reports the highest number of events 
    for Kyushu (134), while GEOFON and USGS report fewer events for the same 
    region. Similar inconsistencies are observed for locations such as 
    Hokkaido, Bonin Islands, Izu Islands, Sea of Japan, and the East Coast 
    of Honshu. These differences indicate that each source uses its own 
    location naming standard.''')

    print('''\n
    5.Most earthquakes reported by EMSC are classified as Weak (147), 
    with fewer Moderate (82) and Strong (2) events. 
    GEOFON and USGS mainly contain Moderate earthquakes, with only a small 
    number of Strong events. 
    MESSY includes only Moderate earthquakes in this dataset.''')

    print('''\n
    Overall, EMSC provides the broadest earthquake coverage, especially for 
    smaller and shallow events, while GEOFON and USGS focus on relatively 
    stronger earthquakes. MESSY contributes fewer but generally deeper events.
    Combining these sources can improve both the completeness and quality of 
    the earthquake database.'''
)

main()
