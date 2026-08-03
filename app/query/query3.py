from sqlalchemy import select , func
from app.database.db_manager import managedb
from app.database.models import Earthquake
from tabulate import tabulate

def rating_dangerous_earthquakes():

    stmt = select(Earthquake.place,
                  Earthquake.category,
                  Earthquake.magnitude,
                  Earthquake.depth)\
                  .where(Earthquake.magnitude > 5 , Earthquake.depth < 50)\
                  .order_by(Earthquake.magnitude.desc(),
                            Earthquake.depth)\
                  .limit(10)
    
    result = managedb.read(stmt,'all_row')   

    return result

def main():

    print('\n === rating the most dangerous earthquakes ===\n ') 

    dangerous_earthquacks = rating_dangerous_earthquakes()

    print(tabulate(dangerous_earthquacks,
                   ['place','category','average_magnitude','average_depth'],
                   tablefmt="heavy_grid"))      
    