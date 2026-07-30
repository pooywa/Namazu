from sqlalchemy import func
from app.database.models import Earthquake
from app.database.configuration import session

def grouping():

    with session as s:

        stmt = s.query(Earthquake.time,Earthquake.category,Earthquake.region)

