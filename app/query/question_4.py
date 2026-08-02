from app.database.models import Earthquake
from app.database.db_manager import managedb
from sqlalchemy import Select,func


def main():

    stmt = Select(Earthquake.source,func.count()).group_by(Earthquake.source).where(Earthquake.category == "Strong")

    earthquakes = managedb.read(stmt,"all_row")

    print("4.Comparison of the number of large earthquakes for each source.?")
    for earthquake in earthquakes:
        print(f"source {earthquake[0]} count: {earthquake[1]}")
