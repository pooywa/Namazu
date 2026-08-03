from sqlalchemy import select, func
from colorama import Fore, Style
from app.database.models import Earthquake
from app.database.db_manager import managedb


def main():
    """
    Question 2:
    Examining the depths at which severe earthquakes typically occur?
    """

    question = (
        "Question 2: Examining the depths at which severe "
        "earthquakes typically occur?"
    )

    print(
        Fore.CYAN +
        Style.BRIGHT +
        question +
        Style.RESET_ALL
    )

    print(
        Fore.GREEN +
        Style.BRIGHT +
        "Answer:" +
        Style.RESET_ALL
    )

    stmt = select(
        func.avg(Earthquake.depth)
    ).where(
        Earthquake.category == "Strong"
    )

    avg_depth = managedb.read(stmt, "one")

    if avg_depth is None:
        print(
            Fore.YELLOW +
            "No data found for strong earthquakes!" +
            Style.RESET_ALL
        )
        return

    print(
        "Strong earthquakes usually occur at a depth of "
        f"{Fore.MAGENTA}{Style.BRIGHT}{avg_depth:.2f}"
        f"{Style.RESET_ALL} kilometers."
    )


if __name__ == "__main__":
    main()