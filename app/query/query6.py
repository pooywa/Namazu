from sqlalchemy import select , func
from app.database.db_manager import managedb
from app.database.models import Earthquake
from tabulate import tabulate

def total_record_of_each_source():

    stmt = select(Earthquake.source,func.count("*"))\
           .group_by(Earthquake.source)

    result = managedb.read(stmt,"all_row")
    return result

def avg_mag_record_of_each_source():

    stmt = select(Earthquake.source,func.avg(Earthquake.magnitude))\
           .group_by(Earthquake.source)

    result = managedb.read(stmt,"all_row")
    return result

def avg_depth_record_of_each_source():

    stmt = select(Earthquake.source,func.avg(Earthquake.depth))\
           .group_by(Earthquake.source)

    result = managedb.read(stmt,"all_row")
    return result

def number_of_record_by_area():
    stmt = select(Earthquake.place,Earthquake.source,func.count("*"))\
               .group_by(Earthquake.place,Earthquake.source)\
               .order_by(Earthquake.place)
    
    result = managedb.read(stmt,"all_row")
    return result

def number_of_each_category():
    stmt = select(Earthquake.source,Earthquake.category,func.count("*"))\
               .group_by(Earthquake.source,Earthquake.category)\
               .order_by(Earthquake.source)
    
    result = managedb.read(stmt,"all_row")
    return result

def main():

    total = total_record_of_each_source()
    print(tabulate(total,
                    ['sources','number of sources'],
                    tablefmt="heavy_grid"))

    avg_mag = avg_mag_record_of_each_source()
    print(tabulate(avg_mag,
                    ['sources','average magnitude of each sources'],
                    tablefmt="heavy_grid"))

    avg_depth = avg_depth_record_of_each_source()
    print(tabulate(avg_depth,
                        ['sources','average depth of each sources'],
                        tablefmt="heavy_grid"))

    area = number_of_record_by_area()
    print(tabulate(area,
                    ['place','source',"number of area"],
                    tablefmt="heavy_grid"))

    category = number_of_each_category()
    print(tabulate(category,
                        ['source','category',"number of category"],
                        tablefmt="heavy_grid"))
