from app.database.db_manager import managedb
from app.database.models import Earthquake
from sqlalchemy import Select,inspect,func
from tabulate import tabulate


sources = ["EMSC","GEOFON","USGS","MESSY"]

def show_tabls_name_type():
    columns = inspect(Earthquake).columns

    result = []
    for c in columns:
        result.append((c.name,c.type))
    print(tabulate(result,['Column Name ','Data Type'],tablefmt="heavy_grid"))

def get_total_column():
    columns = inspect(Earthquake).columns
    print("Total columns:",len(columns))

def record_count():
    # total_record = 0

    # print("| Source | Records |")
    # for source in sources: 
    #     stmt = Select(Earthquake).where(Earthquake.source == source)
    #     r_c =  managedb.read(stmt,"all")
    #     total_record += len(r_c)
    #     print(f"| {source}   | {len(r_c)} |")

    # print("")
    # print("Total records: ",total_record)

    stmt = Select(Earthquake.source,func.count('*')).group_by(Earthquake.source)
    r_c =  managedb.read(stmt,"all_row")

    print(tabulate(r_c,["source","record"],tablefmt="heavy_grid"))

    total_record = sum(row[1] for row in r_c)
    print("\nTotal records: ",total_record)

def null_count():
    cols = Earthquake.__table__.columns

    # print("| Column | NULL Count |")
    # for c in columns:
    #     stmt = Select(func.count()).where(c.is_(None))
    #     count = managedb.read(stmt,"all")
    #     print(f"| {c.name} | {count} |")

    stmt = Select(*[ func.count("*") - func.count(col) for col in cols])
    result = managedb.read(stmt, "all_row")
    
    print(
        tabulate(
            [result],
            headers=[cols.id,cols.place],
            tablefmt="heavy_grid"
        )
    )
def example_data():

    for source in sources:
        stmt = Select(Earthquake).where(Earthquake.source == source)
        earthquake:Earthquake = managedb.read(stmt,"first") 
        print("")
        print(f"example of {source}")
        if earthquake:
             print(
            tabulate(
                [[
                    earthquake.time,
                    earthquake.latitude,
                    earthquake.longitude,
                    earthquake.magnitude,
                    earthquake.place,
                ]],
                headers=["time", "latitude", "longitude", "magnitude", "place"],
                tablefmt="heavy_grid",
            )
        )
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