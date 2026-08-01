from sqlalchemy import Select,inspect
from app.database.db_manager import managedb
from app.database.models import Earthquake
from app.database.configuration import session
from dateutil import parser
import re
from datetime import timezone

def handel_date_format():
    stmt = Select(Earthquake)
    earthquakes:list[Earthquake] = managedb.read(stmt,"all")
    if earthquakes:

        for earthquake in earthquakes:
            time_str = earthquake.time
        
            time_str = re.sub(r"\s+\d+\s+hr\s+\d+\s+min\s+ago$", "", time_str)
        
            use_dayfirst = True if "/" in time_str else False
            parsed_time = parser.parse(time_str, dayfirst=use_dayfirst)

            if parsed_time.tzinfo is None:
                parsed_time = parsed_time.replace(tzinfo=timezone.utc)
            else:
                parsed_time = parsed_time.astimezone(timezone.utc)

            managedb.update(object=earthquake,attr="time",new_value=parsed_time)
        print("update formated time successfuly")


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
                managedb.update(attr="depth",new_value=earthquake.depth.replace("-",""),object=earthquake)
                # managedb.delete(object=earthquake)
                print(f"remove earthquake with negative depth id:{earthquake.id}")

def remove_dublications_and_invalid_data():

    nots_to_remove = ["DUPLICATE","Possible Duplicate"]

    for text in nots_to_remove:
        stmt = Select(Earthquake).where(Earthquake.notes == text)
        earthquakes = managedb.read(stmt,"all")
        if earthquakes:
            for earthquake in earthquakes:
                managedb.delete(object=earthquake)


def mile_to_km(mile:int):
    km = 1.609344
    return round(mile * km,2)

def mtr_to_km(mtr:int):
    return round(mtr/1000,2)


def replace_curent_data():
    char_num = {"one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9"}
    columns = inspect(Earthquake).columns

    for column in columns:
            
        match str(column.name):
            case "magnitude":
                stmt = Select(Earthquake).where(Earthquake.magnitude.op("~")(r"[A-Za-z]"))
                earthquakes = managedb.read(stmt,"all")
                if earthquakes:
                    for earthquake in earthquakes:
                        text = earthquake.magnitude.strip().lower()
                        new_val = None

                        if "." in text:
                            left, right = text.split(".")
                            if left in char_num and right in char_num:
                                new_val = f"{char_num[left]}.{char_num[right]}"

                        elif " " in text:
                            parts = text.split()
                            if (
                                len(parts) == 3
                                and parts[0] in char_num
                                and parts[1] == "point"
                                and parts[2] in char_num
                            ):
                                new_val = f"{char_num[parts[0]]}.{char_num[parts[2]]}"

                        elif text in char_num:
                            new_val = char_num[text]

                        if new_val == None:
                            managedb.delete(object=earthquake)
                            print(f"remove record with id {earthquake.id}")
                        else:
                            managedb.update(object=earthquake,attr="magnitude",new_value=new_val)
                            print(f"update record with id {earthquake.id} new value is {new_val}")

            case "depth":
                stmt = Select(Earthquake).where(Earthquake.depth.op("~")(r"[A-Za-z]"))
                earthquakes = managedb.read(stmt,"all")
                if earthquakes:
                    for earthquake in earthquakes:
                        text:str = earthquake.depth.strip()
                        new_value = None
                        if " " in text:
                            left,right = text.split(" ")

                            if left.isnumeric():
                                if right == "miles":
                                    new_value = mile_to_km(int(left))
                                elif right == "meters":
                                    new_value = mtr_to_km(int(left))
                                elif right == "km":
                                    new_value = float(int(left))

                        if new_value == None:
                            managedb.delete(object=earthquake)
                            print(f"remove record with id {earthquake.id}")
                        else:
                            managedb.update(object=earthquake,attr="depth",new_value=new_value)
                            print(f"update record with id {earthquake.id} new value is {new_value}")

def main():
    print("-------validated format------")
    remove_invalid_records()
    not_be_nigative()
    remove_dublications_and_invalid_data()
    replace_curent_data()
    handel_date_format()
    print("")

if __name__ == "__main__":
    main()