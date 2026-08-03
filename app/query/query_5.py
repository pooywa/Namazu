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
            "No earthquakes found." +
            Style.RESET_ALL
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
        f"Japan had "
        f"{Fore.YELLOW}{Style.BRIGHT}{stats.total_quakes}"
        f"{Style.RESET_ALL} earthquakes."
    )

    print(
        f"Average magnitude: "
        f"{Fore.MAGENTA}{Style.BRIGHT}{avg_mag:.2f}"
        f"{Style.RESET_ALL}"
    )

    print(
        f"Average depth: "
        f"{Fore.BLUE}{Style.BRIGHT}{avg_depth:.2f} km"
        f"{Style.RESET_ALL}"
    )

    print(
        f"Highest concentration: "
        f"{Fore.YELLOW}{Style.BRIGHT}{top_region}"
        f"{Style.RESET_ALL}"
    )


    if avg_mag < 5:
        print(
            Fore.GREEN +
            "Conclusion: Japan experienced "
            "continuous minor and moderate seismic activity."
            + Style.RESET_ALL
        )
    else:
        print(
            Fore.RED +
            "Conclusion: High seismic activity detected."
            + Style.RESET_ALL
        )

    print()


def main():

    with Session(engine) as session:
        analyze_japan_recent_quakes(session)


if __name__ == "__main__":
    main()