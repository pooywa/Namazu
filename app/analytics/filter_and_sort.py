from sqlalchemy import func , select
from app.database.models import Earthquake
from app.database.db_manager import managedb
from tabulate import tabulate

def ten_recent_earthquakes():
    
    stmt =  select(Earthquake)\
            .where(Earthquake.magnitude > 6)\
            .order_by(Earthquake.time.desc(),Earthquake.magnitude.desc())\
            .limit(10)
    
    result = managedb.read(stmt,'all')
    return result

# def depth_and_mag():
    
#         stmt =  select(Earthquake)\
#                 .where(Earthquake.magnitude > 6,Earthquake.depth < 50)

#         result = managedb.read(stmt,'all')
#         return result

# def Record_count_for_each_source():
      
#       stmt =  select(Earthquake.source,func.count("*"))\
#               .group_by(Earthquake.source)
      
#       result = managedb.read(stmt,'all')
#       return result

# def Average_magnitude_grouped_by():

#     stmt =  select(Earthquake.region,Earthquake.source,func.avg(Earthquake.magnitude).label("avg_magnitude"))\
#             .group_by(Earthquake.region,Earthquake.source).order_by(func.avg(Earthquake.magnitude).desc())

#     result = managedb.read(stmt,'all')
#     return result

def main():

        result1 = ten_recent_earthquakes() 
        print("=== Ten Most Recent Strong Earthquakes ===") 
        print(tabulate(result1,headers=["id","time","latetude","longitude","depth","magnitude","place","source","month","category","rigen","nots"],tablefmt="grid"))

#     result2 = depth_and_mag()
#     print("=== Earthquakes With Magnitude > 6 and Depth < 50 km ===")
#     print(result2)
# #     print(tabulate(result2,headers=["id","time","latetude","longitude","depth","magnitude","place","source","month","category","rigen","nots"],tablefmt="grid"))

#     result3 = Record_count_for_each_source()
#     print("=== Record Count by Source ===")
#     print(result3)
# #     print(tabulate(result3,headers=["source","numbers of source"],tablefmt="grid"))


#     result4 = Average_magnitude_grouped_by()
#     print("=== Average Magnitude by Region and Source ===")
#     print(result4)
# #     print(tabulate(result4,headers=["region","source","avarage"],tablefmt="grid"))
