from app.database.models import Earthquake
from app.database.db_manager import managedb
from sqlalchemy import Select, func
from colorama import Fore, Style


def main():

    stmt = Select(
        Earthquake.source,
        func.count()
    ).group_by(
        Earthquake.source
    ).where(
        Earthquake.category == "Strong"
    )

    earthquakes = managedb.read(stmt, "all_row")

    print(
        Fore.CYAN +
        Style.BRIGHT +
        "4. Comparison of the number of large earthquakes for each source.?" +
        Style.RESET_ALL
    )

    print(
        Fore.GREEN +
        Style.BRIGHT +
        "Answer:" +
        Style.RESET_ALL
    )

    for earthquake in earthquakes:
        print(
            f"Source "
            f"{Fore.YELLOW}{earthquake[0]}{Style.RESET_ALL} "
            f"count: "
            f"{Fore.MAGENTA}{earthquake[1]}{Style.RESET_ALL}"
        )


# if __name__ == "__main__":
#     main()