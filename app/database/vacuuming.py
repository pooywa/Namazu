import requests
import time
import pandas as pd
from pathlib import Path

def fix_lat_and_lon(out,file_path):
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
    
        sort_dataFrame_by_null = df[df_result]
    
        for index, row in sort_dataFrame_by_null.iterrows():
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
        df.to_csv(file_path,index=False)

        return df

def fix_attr_data(out,attr):
    print("geting data from csv...")
    df = out
    time.sleep(1)

    df[attr] = pd.to_numeric(df[attr], errors="coerce").astype(float)

    if attr == "depth":
        mean = df.loc[(df[attr] >= 0) & (df[attr] <= 500),attr].mean()
    else:
        mean = round(df.loc[(df[attr] >= 0) & (df[attr] <= 10),attr].mean(),1)

    print(f"filling the missing {attr} data by the avarage of the {attr}...")
    print("attr:", attr)
    print("dtype:", df[attr].dtype)
    print("mean:", mean)
    print(df[attr].head())
    df.loc[df[attr].isna(),attr] = float(mean)
    time.sleep(1)

    print("data updated.")

    return df
   

def vacuuming(out,file_path):

    fix_magnitude = fix_attr_data(out,"magnitude")

    fix_depth = fix_attr_data(fix_magnitude,"depth")

    final_result = fix_lat_and_lon(fix_depth,file_path)

    return final_result