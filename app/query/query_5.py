import datetime
from app.database.configuration import engine
from sqlalchemy import func, select, desc
from sqlalchemy.orm import Session
from colorama import Fore, Style
from app.database.models import Earthquake


def analyze_japan_recent_quakes(session: Session):
    """
    Question 5:
    Scientific conclusion about Japan seismic behavior.
    """

    question = (
        "Question 5: What is the scientific conclusion "
        "regarding Japan's seismic behavior in the last month?"
    )

    print(Fore.CYAN + Style.BRIGHT + question)
    print(Fore.GREEN + "Answer:")


    thirty_days_ago = (
        datetime.datetime.now()
        - datetime.timedelta(days=30)
    )


    stats_stmt = select(
        func.count(Earthquake.id).label("total_quakes"),
        func.avg(Earthquake.magnitude).label("avg_magnitude"),
        func.avg(Earthquake.depth).label("avg_depth")
    ).where(
        Earthquake.region.ilike("%Japan%"),
        Earthquake.time >= thirty_days_ago
    )


    stats = session.execute(stats_stmt).one()


    if stats.total_quakes == 0:
        print(
            Fore.YELLOW +
            "No earthquakes found."
        )
        return



    region_stmt = select(
        Earthquake.region,
        func.count(Earthquake.id).label("region_count")
    ).where(
        Earthquake.region.ilike("%Japan%"),
        Earthquake.time >= thirty_days_ago
    ).group_by(
        Earthquake.region
    ).order_by(
        desc("region_count")
    ).limit(1)


    top_region_row = session.execute(
        region_stmt
    ).first()


    top_region = (
        top_region_row.region
        if top_region_row
        else "Unknown"
    )


    avg_mag = stats.avg_magnitude or 0
    avg_depth = stats.avg_depth or 0


    print(
        f"Japan had {Fore.YELLOW}"
        f"{stats.total_quakes}"
        f"{Fore.RESET} earthquakes."
    )

    print(
        f"Average magnitude: "
        f"{Fore.YELLOW}{avg_mag:.2f}"
        f"{Fore.RESET}"
    )

    print(
        f"Average depth: "
        f"{Fore.YELLOW}{avg_depth:.2f} km"
        f"{Fore.RESET}"
    )

    print(
        f"Highest concentration: "
        f"{Fore.YELLOW}{top_region}"
        f"{Fore.RESET}"
    )


    if avg_mag < 5:
        print(
            "Conclusion: Japan experienced "
            "continuous minor and moderate seismic activity."
        )
    else:
        print(
            "Conclusion: High seismic activity detected."
        )

    print()


if __name__ == "__main__":

    with Session(engine) as session:
        analyze_japan_recent_quakes(session)