from sqlalchemy import select, func
from app.database.models import Earthquake
from app.database.db_manager import managedb


def earthquakes_by_month():
    stmt = (
        select(
            Earthquake.month,
            func.count().label("earthquake_count")
        )
        .group_by(Earthquake.month)
        .order_by(Earthquake.month)
    )

    return managedb.session.execute(stmt).all()


def earthquakes_by_region():
    stmt = (
        select(
            Earthquake.region,
            func.count().label("earthquake_count")
        )
        .where(
            Earthquake.region.is_not(None),
            Earthquake.region != ""
        )
        .group_by(Earthquake.region)
        .order_by(Earthquake.region)
    )

    return managedb.session.execute(stmt).all()


def average_magnitude_by_region():
    stmt = (
        select(
            Earthquake.region,
            func.round(func.avg(Earthquake.magnitude), 2).label("avg_magnitude")
        )
        .where(
            Earthquake.region.is_not(None),
            Earthquake.region != ""
        )
        .group_by(Earthquake.region)
        .order_by(Earthquake.region)
    )

    return managedb.session.execute(stmt).all()


def average_depth_by_region():
    stmt = (
        select(
            Earthquake.region,
            func.round(func.avg(Earthquake.depth), 2).label("avg_depth")
        )
        .where(
            Earthquake.region.is_not(None),
            Earthquake.region != ""
        )
        .group_by(Earthquake.region)
        .order_by(Earthquake.region)
    )

    return managedb.session.execute(stmt).all()


def maximum_magnitude_by_region():
    stmt = (
        select(
            Earthquake.region,
            func.max(Earthquake.magnitude).label("max_magnitude")
        )
        .where(
            Earthquake.region.is_not(None),
            Earthquake.region != ""
        )
        .group_by(Earthquake.region)
        .order_by(Earthquake.region)
    )

    return managedb.session.execute(stmt).all()


def minimum_depth_by_region():
    stmt = (
        select(
            Earthquake.region,
            func.min(Earthquake.depth).label("min_depth")
        )
        .where(
            Earthquake.region.is_not(None),
            Earthquake.region != ""
        )
        .group_by(Earthquake.region)
        .order_by(Earthquake.region)
    )

    return managedb.session.execute(stmt).all()


def maximum_depth_by_region():
    stmt = (
        select(
            Earthquake.region,
            func.max(Earthquake.depth).label("max_depth")
        )
        .where(
            Earthquake.region.is_not(None),
            Earthquake.region != ""
        )
        .group_by(Earthquake.region)
        .order_by(Earthquake.region)
    )

    return managedb.session.execute(stmt).all()


def total_records():
    stmt = select(func.count(Earthquake.id))
    return managedb.session.execute(stmt).scalar()


def main():
    print("=== Earthquake Count By Month ===")
    for row in earthquakes_by_month():
        print(row)

    print("\n=== Earthquake Count By Region ===")
    total = 0
    for region, count in earthquakes_by_region():
        print(region, count)
        total += count

    print("\n=== Average Magnitude By Region ===")
    for row in average_magnitude_by_region():
        print(row)

    print("\n=== Average Depth By Region ===")
    for row in average_depth_by_region():
        print(row)

    print("\n=== Maximum Magnitude By Region ===")
    for row in maximum_magnitude_by_region():
        print(row)

    print("\n=== Minimum Depth By Region ===")
    for row in minimum_depth_by_region():
        print(row)

    print("\n=== Maximum Depth By Region ===")
    for row in maximum_depth_by_region():
        print(row)

    print("\nGrouped Count :", total)
    print("Table Count   :", total_records())


if __name__ == "__main__":
    main()