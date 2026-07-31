from sqlalchemy import func , select
from app.database.models import Earthquake
from app.database.db_manager import managedb
from tabulate import tabulate

def grouping():

            stmt = select(Earthquake.month,
                          Earthquake.category,
                          Earthquake.region,
                          func.count("*").label("earthquake_count"),
                          func.avg(Earthquake.magnitude).label("avg_magnitude"),
                          func.avg(Earthquake.depth).label("avg_depth"))\
                    .group_by(Earthquake.month,
                              Earthquake.category,
                              Earthquake.region)\
                    .order_by(Earthquake.month,
                              Earthquake.region,
                              Earthquake.category)

            result =  managedb.read(stmt,'all_row')
            return result


def main():

    # with tabulate we print our results in a pretty way
    result = grouping()
    
    print(tabulate(result,
                   headers=['month',
                            'category',
                            'region',
                            'earthquake_count',
                            'avg_magnitude',
                            'avg_depth'],
                    tablefmt="grid"))

  

