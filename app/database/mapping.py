from pathlib import Path

COLLECTOR_MAPPING = {
    "DateTime": "time",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Depth(km)": "depth",
    "Magnitude": "magnitude",
    "Region": "place",
}

MESSY_MAPPING = {
    "time": "time",
    "latitude": "latitude",
    "longitude": "longitude",
    "depth": "depth",
    "mag": "magnitude",
    "place": "place",
}

MAPPINGS = {
    "MESSY": MESSY_MAPPING,
}


def detect_source(filename: str) -> str:
    name_upper = Path(filename).name.upper()
    if "USGS" in name_upper:
        return "USGS"
    if "EMSC" in name_upper:
        return "EMSC"
    if "GEOFON" in name_upper:
        return "GEOFON"
    if "DATASET" in name_upper or "MESSY" in name_upper:
        return "MESSY"
    raise ValueError(f"Cannot determine source from filename: {filename}")


def map_row(row: dict, source: str, filename: str = "unknown_file.csv") -> dict:
    mapping = MAPPINGS.get(source, COLLECTOR_MAPPING)

    try:
        mapped = {db_col: row[csv_col] for csv_col, db_col in mapping.items()}
    except KeyError as e:
        missing_col = e.args[0]
        raise ValueError(
            f"Validation Error in {filename}: missing required column "
            f"'{missing_col}' for source {source}"
        ) from e

    mapped["source"] = source
    return mapped