from sqlalchemy import select,extract,update
from app.database.configuration import session
from app.database.db_manager import managedb
from app.database.models import Earthquake
import re

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
    stmt = select(Earthquake)

    result = managedb.read(stmt,"all")

    for place in result:

        if "," in place.place:
            first_part_of_place = place.place.strip().lower().split(",")[0]

            if 'km' in first_part_of_place:
                region = first_part_of_place.strip().split(" ")[-1]

                managedb.update('region',region,object=place)

            else:
                managedb.update('region',first_part_of_place,object=place)
            
        else:
            managedb.update('region',place.place,object=place)

def main():

    add_month_to_table()

    add_label_of_categury()

    add_rigion_finder()