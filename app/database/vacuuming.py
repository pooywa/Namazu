import requests
import time
import pandas as pd

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

def fix_the_mag(out):
     pass

def vacuuming(out):
    
    fix_lan_and_lon(out)

    fix_the_mag(out)