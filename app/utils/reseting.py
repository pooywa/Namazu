from app.database import configuration
from app.database.models import Earthquake
from pathlib import Path

def reset_db():

    try:
        configuration.session.close()
        Earthquake.metadata.drop_all(configuration.engine)
        configuration.engine.dispose()
        print("table drop successfuly")
    except Exception as e:
        pass

def remove_csv():

    print("starting remove the old files")

    file_names = ["emsc-earthquakes.csv","geofon-earthquakes.csv","usgs-earthquakes.csv"]

    for file_name in file_names:
        path = Path(f"data/raw/{file_name}")
        if path.exists():
            path.unlink()

    print("files removed")


def main():

    try:

        reset_db()
        remove_csv()
    except Exception as e:
        print(f"error:{e}")