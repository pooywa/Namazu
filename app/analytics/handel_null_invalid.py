from sqlalchemy import Select,inspect
from app.database.db_manager import managedb
from app.database.models import Earthquake
from app.database.configuration import session


remove_if_is_none_column = ["time","latitude","longitude","depth","magnitude"]

def remove_invalid_records():

    columns = inspect(Earthquake).columns
    for column in columns:
        if str(column.name) in remove_if_is_none_column:
            stmt = Select(Earthquake).where(column.is_(None))
            invalid_earthquakes = managedb.read(stmt,"all")
            for earthquake in invalid_earthquakes:
                if earthquake:
                    managedb.delete(object=earthquake)
                    print(f"remove earthquake:",earthquake.id)

def set_unknown():

    stmt = Select(Earthquake).where(Earthquake.place.is_(None))
    earthquakes = managedb.read(stmt,"all")
    if earthquakes:
        managedb.update(object=earthquakes,attr="place",new_value="unknown")


not_negative_columns = [Earthquake.depth]
def not_be_nigative():

    for column in not_negative_columns:
        stmt = Select(Earthquake).where(column.contains("-"))
        earthquakes = managedb.read(stmt,"all")
        for earthquake in earthquakes:
            if earthquake:
                managedb.delete(object=earthquake)
                print(f"remove earthquake with negative depth id:{earthquake.id}")




    



def main():
    remove_invalid_records()
    not_be_nigative()

if __name__ == "__main__":
    main()