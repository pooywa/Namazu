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

def add_label_of_category():
    stmt = select(Earthquake)
    magnitudes = managedb.read(stmt,"all")

    for magnitude in magnitudes:
        if magnitude.magnitude < 4:
            managedb.update(attr="category",new_value="Weak",object=magnitude)
        elif 4 <=magnitude.magnitude <= 6:
            managedb.update(attr="category",new_value="Moderate",object=magnitude)
        else:
            managedb.update(attr="category",new_value="Strong",object=magnitude)
    

def add_rigion_finder():
    stmt = select(Earthquake)

    result = managedb.read(stmt,"all")

    for place in result:

        if "," in place.place:
            first_part_of_place = place.place.strip().lower().split(",")[0]

            if re.search(r"\d+|\bkm\b", first_part_of_place):
                region = first_part_of_place.strip().split(" ")[-1]

                managedb.update(attr='region',new_value=region,object=place)

            else:
                managedb.update(attr='region',new_value=first_part_of_place,object=place)
            
        else:
            managedb.update(attr='region',new_value=place.place,object=place)

def main():

    try:
        add_month_to_table()
        print("month add successfuly")

        add_label_of_category()
        print("label of category add successfuly")

        add_rigion_finder()
        print("rigion add successfuly")

    except Exception as e :
        print(f"error: {e}")
