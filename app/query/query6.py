from sqlalchemy import select, func
from app.database.db_manager import managedb
from app.database.models import Earthquake
from tabulate import tabulate
from colorama import Fore, Style
from collections import defaultdict


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
            "Question 6: sugestion for combinng sources to optimize the quiality of all data?" +
            Style.RESET_ALL
        )
       

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

    print(tabulate(category,
                        ['source','category',"number of category"],
                        tablefmt="heavy_grid"))


    # -------------------- Analysis Summary --------------------

    top_source = max(total, key=lambda x: x[1])

    print(
        f"\n1. {top_source[0]} provides the largest number of earthquake "
        f"records ({top_source[1]}), making it the primary data source."
    )

    highest_mag = max(avg_mag, key=lambda x: x[1])
    lowest_mag = min(avg_mag, key=lambda x: x[1])

    print(
        f"\n2. {highest_mag[0]} reports the highest average earthquake "
        f"magnitude ({highest_mag[1]:.2f}), while {lowest_mag[0]} has the "
        f"lowest average magnitude ({lowest_mag[1]:.2f})."
    )

    deepest = max(avg_depth, key=lambda x: x[1])
    shallowest = min(avg_depth, key=lambda x: x[1])

    print(
        f"\n3. {deepest[0]} reports the deepest earthquakes on average "
        f"({deepest[1]:.2f} km), while {shallowest[0]} reports the "
        f"shallowest earthquakes ({shallowest[1]:.2f} km)."
    )

    print("\n4. Earthquake categories by source:")

    summary = defaultdict(dict)

    for source, category_name, count in category:
        summary[source][category_name] = count

    for source, values in summary.items():
        print(
            f"   {source}: "
            f"Weak={values.get('Weak', 0)}, "
            f"Moderate={values.get('Moderate', 0)}, "
            f"Strong={values.get('Strong', 0)}"
        )

    print(
        f"\n5. Overall, {top_source[0]} provides the broadest earthquake "
        f"coverage. {highest_mag[0]} reports the highest average magnitude, "
        f"while {deepest[0]} records the deepest earthquakes."
    )