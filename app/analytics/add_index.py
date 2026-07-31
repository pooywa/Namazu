from sqlalchemy import create_engine, text
from app.database.configuration import session

indexes = {
    "idx_earthquakes_region": "region",
    "idx_earthquakes_time": "time",
    "idx_earthquakes_magnitude": "magnitude",
}

def main():
    with session:
        for name, col in indexes.items():
            session.execute(text(f"CREATE INDEX IF NOT EXISTS {name} ON earthquakes({col});"))
        session.commit()

        
        test = session.execute(text("SELECT * FROM earthquakes LIMIT 1;")).fetchone()
        print("tables:", test is not None)

        
        result = session.execute(text(
            "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'earthquakes' ORDER BY indexname;"
        ))
        print("\n indexes earthquakes:")
        for row in result:
            print(f"  {row.indexname} -> {row.indexdef}")