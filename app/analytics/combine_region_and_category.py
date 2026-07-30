from sqlalchemy import func , select
from app.database.models import Earthquake
from app.database.configuration import session
from tabulate import tabulate

def grouping(session):

    with session:
        try:
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

            result = session.execute(stmt).all()
            return result
        except Exception as e:
            print(e)
            return []

def main():

    # with tabulate we print our results in a pretty way
    result = grouping(session)
    print(tabulate(result,
                   headers=['month',
                            'category',
                            'region',
                            'earthquake_count',
                            'avg_magnitude',
                            'avg_depth'],
                    tablefmt="grid"))

        

