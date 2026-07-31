from sqlalchemy import select,extract,update
from app.database.configuration import session
from app.database.db_manager import managedb
from app.database.models import Earthquake

def add_month_to_table():

    stmt = update(Earthquake)\
           .values(month=extract("month", Earthquake.time))

    with session:
        session.execute(stmt)
        session.commit()

def add_label_of_categury():
    stmt = select(Earthquake)
    magnitudes = managedb.read(stmt,"all")

    for magnitude in magnitudes:
        if magnitude.magnitude < 4:
            managedb.update("category","Weak",object=magnitude)
        elif 4 <=magnitude.magnitude <= 6:
            managedb.update("category","Moderate",object=magnitude)
        else:
            managedb.update("category","Strong",object=magnitude)
    

def add_rigion_finder():
    pass

def main():

    add_month_to_table()

    add_label_of_categury()

    add_rigion_finder()