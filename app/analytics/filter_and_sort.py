from sqlalchemy import func , select
from app.database.models import Earthquake
from app.database.configuration import session
from tabulate import tabulate

def ten_recent_earthquakes(session):
    with session:
        stmt =  select(Earthquake)\
                .where(Earthquake.magnitude == "Strong")\
                .order_by(Earthquake.time)\
                .limit(10)

        result = session.execute(stmt).all()

