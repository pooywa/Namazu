from sqlalchemy import Select,text
from app.database.models import Earthquake
from app.database.db_manager import managedb
from app.database.preview_data import show_tabls_name_type
from app.utils import restart_engine

def conver_to_float():

    stmt = Select(Earthquake)
    earthquakes:list[Earthquake] = managedb.read(stmt,"all")
    if earthquakes:
        for earthquake in earthquakes:
            depth_val = str(float(earthquake.depth))
            mag_val = str(float(earthquake.magnitude))

            managedb.update(object=earthquake,attr="depth",new_value=depth_val)
            managedb.update(object=earthquake,attr="magnitude",new_value=mag_val)
        print("convert depth and magnitude to float successfuly")

def convert_table_type():
    mag_text = """ALTER TABLE earthquakes
ALTER COLUMN magnitude TYPE DOUBLE PRECISION
USING magnitude::DOUBLE PRECISION;"""    

    depth_text = """ALTER TABLE earthquakes
ALTER COLUMN depth TYPE DOUBLE PRECISION
USING depth::DOUBLE PRECISION;"""

    time_text = """ALTER TABLE earthquakes
ALTER COLUMN time TYPE TIMESTAMP
USING time::TIMESTAMP;"""

    list_text = [mag_text,depth_text,time_text]

    with managedb.session as session:
        for txt in list_text:
            session.execute(text(txt))
            session.commit()

    print("table type successfuly changed ")
    restart_engine.restart_en()


def main():
    conver_to_float()
    convert_table_type()

if __name__ == "__main__":
    main()
    
