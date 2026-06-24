import requests
import pandas as pd
import os

# Create raw folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

schemes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        df = pd.DataFrame(data["data"])

        df.to_csv(f"data/raw/{name}.csv", index=False)

        print(f"{name}.csv saved successfully")

    else:
        print(f"Failed for {name}")