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
    pass
    

def add_rigion_finder():
    pass

def main():

    add_month_to_table()

    add_label_of_categury()

    add_rigion_finder()