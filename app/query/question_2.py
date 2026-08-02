from app.database.models import Earthquake
from app.database.db_manager import managedb
from sqlalchemy import Select,func

def main():

    stmt = Select(func.avg(Earthquake.depth)).where(Earthquake.category == "Strong")
    avg_depth = managedb.read(stmt,"one")

    print("2.Examining the depths at which severe earthquakes typically occur.?")
    print(f"It usually occurs at a depth of {avg_depth} kilometers.")
