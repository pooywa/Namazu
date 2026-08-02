from app.database.db_manager import managedb
from app.database.models import Earthquake
from sqlalchemy import Select,inspect,func


sources = ["EMSC","GEOFON","USGS","MESSY"]

def show_tabls_name_type():
    columns = inspect(Earthquake).columns

    print("| Column Name | Data Type |")
    print("|-------------|-----------|")
    for c in columns:
        print(f"| {c.name}          | {c.type} |")

def get_total_column():
    columns = inspect(Earthquake).columns
    print("Total columns:",len(columns))

def record_count():
    total_record = 0

    print("| Source | Records |")
    for source in sources: 
        stmt = Select(Earthquake).where(Earthquake.source == source)
        r_c =  managedb.read(stmt,"all")
        total_record += len(r_c)
        print(f"| {source}   | {len(r_c)} |")

    print("")
    print("Total records: ",total_record)

def null_count():
    columns = inspect(Earthquake).columns

    print("| Column | NULL Count |")
    for c in columns:
        stmt = Select(func.count()).where(c.is_(None))
        count = managedb.read(stmt,"all")
        print(f"| {c.name} | {count} |")

def example_data():

    for source in sources:
        stmt = Select(Earthquake).where(Earthquake.source == source)
        earthquake:Earthquake = managedb.read(stmt,"first") 
        print("")
        print(f"example of {source}")
        if earthquake:
            print("| time | latitude | longitude | magnitude | place |")
            print(f"| {earthquake.time } | {earthquake.latitude } | {earthquake.longitude } | {earthquake.magnitude } | {earthquake.place } |")
        else:
            print("table is empty")


def main():

    print("----Show Tabls and types")
    show_tabls_name_type()
    print("")
    print("----Total Column")
    get_total_column()
    print("")
    print("----Record Count")
    record_count()
    print("")
    print("----Null Count")
    null_count()
    print("")

    print("----Example Data")
    example_data()

if __name__ == "__main__":
    main()