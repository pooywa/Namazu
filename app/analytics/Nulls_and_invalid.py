from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.configuration import session,engine


# counting the number of nulls
def count_null(session):
    
    count = session.execute(text('''
                            SELECT count(*)
                            FROM earthquakes
                            where time is null or
                            Latitude is null or
                            Longitude is null or
                            Depth is null or
                            Magnitude is null or 
                            Region is null
                        ''')).scalar()

    print(f"the number of row that contain null {count}")
