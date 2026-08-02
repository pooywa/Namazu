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

    print(Fore.CYAN + Style.BRIGHT + question)
    print(Fore.GREEN + "Answer:")

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
            "No data found for small earthquakes!"
        )
        return

    print("Based on extracted data:")

    for row in results:
        print(
            f"- Source {Fore.YELLOW}{row.source}{Fore.RESET}: "
            f"{row.small_quakes_count} events | "
            f"Min magnitude: {row.min_magnitude} | "
            f"Mean magnitude: {row.mean_magnitude:.2f}"
        )

    print()


if __name__ == "__main__":

    with Session(engine) as session:
        analyze_small_quakes(session)