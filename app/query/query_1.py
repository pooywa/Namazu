from sqlalchemy import func, select
from sqlalchemy.orm import Session
from colorama import Fore, Style
from app.database.configuration import engine
from app.database.models import Earthquake


def analyze_small_quakes(session: Session):
    """
    Question 1:
    How do different sources cover small events (magnitude < 4)?
    """

    question = (
        "Question 1: How do different sources cover small events "
        "(magnitude < 4), and what are the differences between them?"
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
        Earthquake.source,
        func.count(Earthquake.id).label("small_quakes_count"),
        func.min(Earthquake.magnitude).label("min_magnitude"),
        func.avg(Earthquake.magnitude).label("mean_magnitude")
    ).where(
        Earthquake.magnitude < 4
    ).group_by(
        Earthquake.source
    )

    results = session.execute(stmt).all()

    if not results:
        print(
            Fore.YELLOW +
            "No data found for small earthquakes!" +
            Style.RESET_ALL
        )
        return

    print(
        Fore.BLUE +
        "Based on extracted data:" +
        Style.RESET_ALL
    )

    for row in results:
        print(
            f"- Source "
            f"{Fore.YELLOW}{Style.BRIGHT}{row.source}{Style.RESET_ALL}: "
            f"{Fore.GREEN}{row.small_quakes_count}{Style.RESET_ALL} events | "
            f"Min magnitude: "
            f"{Fore.MAGENTA}{row.min_magnitude}{Style.RESET_ALL} | "
            f"Mean magnitude: "
            f"{Fore.CYAN}{row.mean_magnitude:.2f}{Style.RESET_ALL}"
        )

    print()


def main():
    with Session(engine) as session:
        analyze_small_quakes(session)


if __name__ == "__main__":
    main()