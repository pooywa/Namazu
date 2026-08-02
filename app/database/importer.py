from pathlib import Path
import pandas as pd
from app.database.vacuuming import vacuuming
from app.database.configuration import engine
from app.database.mapping import COLLECTOR_MAPPING, MAPPINGS, detect_source
from app.database.models import Earthquake

TABLE_NAME = "earthquakes"
CHUNK_SIZE = 100

def import_one_file(file_path: Path) -> int:
    filename = file_path.name
    source = detect_source(filename)
    mapping = MAPPINGS.get(source, COLLECTOR_MAPPING)
    required_cols = list(mapping.keys())

    imported_rows = 0

    for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):
        out = chunk[required_cols].rename(columns=mapping).copy()
        out["source"] = source

        #here we clean the data
        cleaned = vacuuming(out,file_path)

        cleaned.to_sql(
            name=TABLE_NAME,
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
        )

        imported_rows += len(out)

    return imported_rows


def main() -> None:
    Earthquake.metadata.create_all(engine)

    csv_files = sorted(Path("data/raw").glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("No CSV files found in data directory.")

    if len(csv_files) != 4:
        raise ValueError(f"Expected 4 CSV files, found {len(csv_files)}.")

    print("Starting import...")
    print("Warning: append mode is used. Start with an empty table to avoid duplicates.\n")

    total_rows = 0

    for file_path in csv_files:
        print(f"Processing {file_path.name} ...")
        rows = import_one_file(file_path)
        print(f"Imported {rows} rows from {file_path.name}\n")
        total_rows += rows

    print(f"Import finished. Total imported rows: {total_rows}")


if __name__ == "__main__":
    main()
