from sqlalchemy import func , select
from app.database.models import Earthquake
from app.database.db_manager import managedb
from tabulate import tabulate

def ten_recent_earthquakes():
    
    stmt =  select(Earthquake)\
            .where(Earthquake.category == "Strong")\
            .order_by(Earthquake.time.desc(),Earthquake.magnitude.desc())\
            .limit(10)
    
    result = managedb.read(stmt,'all')
    return result

def depth_and_mag():
    
        stmt =  select(Earthquake)\
                .where(Earthquake.category == "strong",Earthquake.depth < 50)

        result = managedb.read(stmt,'all')
        return result

def Record_count_for_each_source():
      
      stmt =  select(Earthquake.source,func.count("*"))\
              .group_by(Earthquake.source)
      
      result = managedb.read(stmt,'all')
      return result

def Average_magnitude_grouped_by():

    stmt =  select(Earthquake.region,Earthquake.source,func.avg(Earthquake.magnitude))\
            .group_by(Earthquake.region,Earthquake.source).order_by(func.avg(Earthquake.magnitude).desc())

    result = managedb.read(stmt,'all')
    return result

def main():

    result1 = ten_recent_earthquakes()
    
    result2 = depth_and_mag()

    result3 = Record_count_for_each_source()

    result4 = Average_magnitude_grouped_by()