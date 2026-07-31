from sqlalchemy import select, func
from app.database.models import Earthquake
from app.database.db_manager import managedb


def earthquakes_by_month():
    stmt = (
        select(
            Earthquake.month,
            func.count().label("earthquake_count"),
        )
        .group_by(Earthquake.month)
        .order_by(Earthquake.month)
    )
    return managedb.session.execute(stmt).all()


def region_stats():
    stmt = (
        select(
            Earthquake.region,
            func.count().label("earthquake_count"),
            func.round(func.avg(Earthquake.magnitude), 2).label("avg_magnitude"),
            func.round(func.avg(Earthquake.depth), 2).label("avg_depth"),
            func.max(Earthquake.magnitude).label("max_magnitude"),
            func.min(Earthquake.depth).label("min_depth"),
            func.max(Earthquake.depth).label("max_depth"),
        )
        .where(
            Earthquake.region.is_not(None),
            Earthquake.region != "",
        )
        .group_by(Earthquake.region)
        .order_by(func.count().desc())
    )
    return managedb.session.execute(stmt).all()


def by_region_month_category():
    stmt = (
        select(
            Earthquake.region,
            Earthquake.month,
            Earthquake.category,
            func.count().label("count"),
            func.round(func.avg(Earthquake.magnitude), 2).label("avg_magnitude"),
            func.round(func.avg(Earthquake.depth), 2).label("avg_depth"),
        )
        .where(
            Earthquake.region.is_not(None),
            Earthquake.region != "",
        )
        .group_by(Earthquake.region, Earthquake.month, Earthquake.category)
        .order_by(Earthquake.region, Earthquake.month, Earthquake.category)
    )
    return managedb.session.execute(stmt).all()


def top_10_recent():
    stmt = (
        select(Earthquake)
        .order_by(Earthquake.time.desc(), Earthquake.magnitude.desc())
        .limit(10)
    )
    return managedb.session.execute(stmt).scalars().all()


def strong_and_shallow():
    stmt = (
        select(Earthquake)
        .where(
            Earthquake.magnitude > 6,
            Earthquake.depth < 50,
        )
        .order_by(Earthquake.magnitude.desc())
    )
    return managedb.session.execute(stmt).scalars().all()


def count_by_source():
    stmt = (
        select(
            Earthquake.source,
            func.count().label("count"),
        )
        .group_by(Earthquake.source)
        .order_by(func.count().desc())
    )
    return managedb.session.execute(stmt).all()


def avg_magnitude_by_region_source():
    stmt = (
        select(
            Earthquake.region,
            Earthquake.source,
            func.round(func.avg(Earthquake.magnitude), 2).label("avg_magnitude"),
            func.count().label("n"),
        )
        .where(
            Earthquake.region.is_not(None),
            Earthquake.region != "",
        )
        .group_by(Earthquake.region, Earthquake.source)
        .order_by(func.avg(Earthquake.magnitude).desc())
    )
    return managedb.session.execute(stmt).all()


def total_records():
    stmt = select(func.count(Earthquake.id))
    return managedb.session.execute(stmt).scalar()


def main():
    print("=== 1. Count by Month ===")
    for row in earthquakes_by_month():
        print(row)

    print("\n=== 2. Region Stats ===")
    for row in region_stats():
        print(row)

    print("\n=== 3. Region + Month + Category ===")
    for row in by_region_month_category():
        print(row)

    # print("\n=== 4. Top 10 Recent ===")
    # for eq in top_10_recent():
    #     print(eq.id, eq.time, eq.magnitude, eq.depth, eq.place, eq.source)

    # print("\n=== 5. Strong & Shallow (mag > 6, depth < 50) ===")
    # rows = strong_and_shallow()
    # if not rows:
    #     print("No matching records")
    # else:
    #     for eq in rows:
    #         print(eq.id, eq.time, eq.magnitude, eq.depth, eq.place, eq.source)

    # print("\n=== 6. Count by Source ===")
    # for row in count_by_source():
    #     print(row)

    # print("\n=== 7. Avg Magnitude by Region + Source ===")
    # for row in avg_magnitude_by_region_source():
    #     print(row)

    print("\n=== Total Records ===")
    print(total_records())


if __name__ == "__main__":
    main()