from sqlalchemy import select, func
from app.database.db_manager import managedb
from app.database.models import Earthquake
from tabulate import tabulate
from colorama import Fore, Style
from collections import defaultdict


def total_record_of_each_source():

    stmt = (
        select(
            Earthquake.source,
            func.count("*")
        )
        .group_by(Earthquake.source)
    )

    return managedb.read(stmt, "all_row")


def avg_mag_record_of_each_source():

    stmt = (
        select(
            Earthquake.source,
            func.avg(Earthquake.magnitude)
        )
        .group_by(Earthquake.source)
    )

    return managedb.read(stmt, "all_row")


def avg_depth_record_of_each_source():

    stmt = (
        select(
            Earthquake.source,
            func.avg(Earthquake.depth)
        )
        .group_by(Earthquake.source)
    )

    return managedb.read(stmt, "all_row")


def number_of_record_by_area():

    stmt = (
        select(
            Earthquake.place,
            Earthquake.source,
            func.count("*")
        )
        .group_by(
            Earthquake.place,
            Earthquake.source
        )
        .order_by(Earthquake.place)
    )

    return managedb.read(stmt, "all_row")


def number_of_each_category():

    stmt = (
        select(
            Earthquake.source,
            Earthquake.category,
            func.count("*")
        )
        .group_by(
            Earthquake.source,
            Earthquake.category
        )
        .order_by(Earthquake.source)
    )

    return managedb.read(stmt, "all_row")


def main():

    print(
        Fore.CYAN +
        Style.BRIGHT +
        "Question 6: Suggestion for combining sources to optimize data quality"
        + Style.RESET_ALL
    )



    total = total_record_of_each_source()
    avg_mag = avg_mag_record_of_each_source()
    avg_depth = avg_depth_record_of_each_source()
    area = number_of_record_by_area()
    category = number_of_each_category()



    print(
        Fore.CYAN +
        Style.BRIGHT +
        "\n=== Total records of each source ===\n" +
        Style.RESET_ALL
    )

    print(
        Fore.YELLOW +
        tabulate(
            total,
            ["Source", "Number of Records"],
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

    print(
        Fore.GREEN +
        tabulate(
            avg_mag,
            ["Source", "Average Magnitude"],
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

    print(
        Fore.BLUE +
        tabulate(
            avg_depth,
            ["Source", "Average Depth"],
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

    print(
        Fore.MAGENTA +
        tabulate(
            area,
            ["Place", "Source", "Number of Records"],
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

    print(
        Fore.YELLOW +
        tabulate(
            category,
            ["Source", "Category", "Number"],
            tablefmt="heavy_grid"
        ) +
        Style.RESET_ALL
    )

    top_source = max(
        total,
        key=lambda x: x[1]
    )

    highest_mag = max(
        avg_mag,
        key=lambda x: x[1]
    )

    lowest_mag = min(
        avg_mag,
        key=lambda x: x[1]
    )

    deepest = max(
        avg_depth,
        key=lambda x: x[1]
    )

    shallowest = min(
        avg_depth,
        key=lambda x: x[1]
    )


    print(
        Fore.CYAN +
        Style.BRIGHT +
        "\n=== Dynamic Analysis Summary ===" +
        Style.RESET_ALL
    )


    print(
        f"""
1. {top_source[0]} provides the largest number of earthquake records
({top_source[1]}), making it the primary data source.
"""
    )


    print(
        f"""
2. {highest_mag[0]} reports the highest average earthquake magnitude
({highest_mag[1]:.2f}), while {lowest_mag[0]} reports the lowest average
magnitude ({lowest_mag[1]:.2f}).
"""
    )


    print(
        f"""
3. {deepest[0]} reports the deepest earthquakes on average
({deepest[1]:.2f} km), while {shallowest[0]} reports the shallowest
earthquakes ({shallowest[1]:.2f} km).
"""
    )


    print(
        "\n4. Earthquake category distribution by source:"
    )

    summary = defaultdict(dict)

    for source, category_name, count in category:
        summary[source][category_name] = count


    for source, values in summary.items():

        print(
            f"""
{source}:
    Weak: {values.get('Weak', 0)}
    Moderate: {values.get('Moderate', 0)}
    Strong: {values.get('Strong', 0)}
"""
        )


    print(
        f"""
5. Overall conclusion:

{top_source[0]} provides the broadest earthquake coverage with
{top_source[1]} recorded events.

{highest_mag[0]} reports the highest average magnitude
({highest_mag[1]:.2f}), while {deepest[0]} records the deepest earthquakes
({deepest[1]:.2f} km).

Combining multiple earthquake sources can improve database completeness,
accuracy, and reliability.
"""
    )
