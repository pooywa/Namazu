from sqlalchemy import select,func,delete
from app.database.db_manager import managedb
from app.database.db_manager import managedb
from app.database.models import Earthquake

def remove_dublicate_records():
    duplicate_ids = (
        select(Earthquake.id)
        .where(
            Earthquake.id.not_in(
                select(func.min(Earthquake.id))
                .group_by(
                    Earthquake.time,
                    Earthquake.latitude,
                    Earthquake.longitude,
                    Earthquake.depth,
                    Earthquake.magnitude,
                    Earthquake.place,
                    Earthquake.source,
                )
            )
        )
    )


    stmt = delete(Earthquake).where(Earthquake.id.in_(duplicate_ids))

    managedb.session.execute(stmt)
    managedb.session.commit()

def main():
    remove_dublicate_records()

if __name__ == "__main__":
    main()