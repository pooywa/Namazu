from pathlib import Path

STANDARD_MAPPING = {
    "DateTime":  "time",
    "Latitude":  "latitude",
    "Longitude": "longitude",
    "Depth(km)": "depth",
    "Magnitude": "magnitude",
    "Region":    "place",
}

MESSY_MAPPING = {
    "time":      "time",
    "latitude":  "latitude",
    "longitude": "longitude",
    "depth":     "depth",
    "mag":       "magnitude",
    "place":     "place",
}

TARGET_COLUMNS = ["time", "latitude", "longitude", "depth", "magnitude", "place", "source"]


def detect_source(filename: str) -> str:
    name = Path(filename).stem.upper()
    if "USGS" in name:
        return "USGS"
    if "EMSC" in name:
        return "EMSC"
    if "GEOFON" in name:
        return "GEOFON"
    if "DATASET" in name or "MESSY" in name:
        return "MESSY"
    raise ValueError(f"Cannot determine source from filename: {filename}")


def get_mapping(filename: str) -> dict:
    source = detect_source(filename)
    if source == "MESSY":
        return MESSY_MAPPING
    return STANDARD_MAPPING

# Map raw CSV rows to the unified database schema and preserve original values.
def map_row(row: dict, filename: str) -> dict:
    source = detect_source(filename)
    mapping = get_mapping(filename)
    record = {col: None for col in TARGET_COLUMNS}
    record["source"] = source
    for csv_col, db_col in mapping.items():
        record[db_col] = row.get(csv_col)
    return record