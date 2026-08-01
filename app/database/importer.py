from pathlib import Path
import pandas as pd
from app.database.configuration import engine
from app.database.mapping import COLLECTOR_MAPPING, MAPPINGS, detect_source
import requests
import time

TABLE_NAME = "earthquakes"
CHUNK_SIZE = 100

def fix_lan_and_lon(out):
        url = "https://nominatim.openstreetmap.org/search"
    
        headers = {
            "User-Agent": "my-earthquake-project"
        }
    
        df = out
    
        delete = []
    
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    
        df_result = (df["latitude"].isna() |
                df["longitude"].isna())
    
        s = df[df_result]
    
        for index, row in s.iterrows():
            place = row["place"]
            params = {"q": place, "format": "json"}
    
            response = requests.get(url, params=params, headers=headers)
    
            if response.status_code != 200:
                print(f"[{place}] request failed: {response.status_code}")
                delete.append(index)
                time.sleep(1)
                continue
    
            r = response.json()
    
            if not r:
                print(f"[{place}] no result found")
                time.sleep(1)
                continue
    
            df.loc[index, "latitude"] = float(r[0]["lat"])
            df.loc[index, "longitude"] = float(r[0]["lon"])
            print(f"[{place}] -> lat={r[0]['lat']}, lon={r[0]['lon']}")
    
            time.sleep(1)  
    
        df = df.drop(index=delete)

def vacuuming(out):
    
    fix_lan_and_lon(out)

    

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
        result = vacuuming(out)

        result.to_sql(
            name=TABLE_NAME,
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
        )

        imported_rows += len(out)

    return imported_rows


def main() -> None:
    csv_files = sorted(Path("data/raw").glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("No CSV files found in data directory.")

    # if len(csv_files) != 4:
    #     raise ValueError(f"Expected 4 CSV files, found {len(csv_files)}.")

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
