from sqlalchemy import Select
from app.database.db_manager import managedb
from app.database.models import Earthquake


MANUAL_MAPPING = {
    "osaka": "Osaka",
    "fukushima prefecture": "Fukushima",
}


def extract_region(place: str) -> str:
    if not place:
        return None

    region = place.strip()
    region = " ".join(region.split())

    if region.lower().startswith("near "):
        region = region[5:]

    if region.lower().endswith(", japan region"):
        region = region[:-15]

    elif region.lower().endswith(", japan"):
        region = region[:-7]
        
    if region.lower().endswith(" prefecture"):
        region = region[:-11]

    region = region.strip()
    region = region.title()
    key = region.lower()

    if key in MANUAL_MAPPING:
        region = MANUAL_MAPPING[key]

    return region


def clean_regions():
    stmt = Select(Earthquake)
    earthquakes = managedb.read(stmt, "all")
    updated = 0
    for earthquake in earthquakes:
        # earthquake.region = extract_region(earthquake.place)
        test = extract_region(earthquake.place)
        updated += 1

    # managedb.session.commit()
    print(f"{updated} regions updated.")


if __name__ == "__main__":
    clean_regions()