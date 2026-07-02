import os
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
LOG_DIR = ROOT / "logs"
RAW_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

SCHEMES = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}


def fetch_nav_history(amfi_code: int) -> pd.DataFrame:
    url = f"https://api.mfapi.in/mf/{amfi_code}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    payload = response.json()
    data = payload.get("data", [])
    if not data:
        raise ValueError(f"No NAV history returned for AMFI code {amfi_code}")

    df = pd.DataFrame(data)
    if {"date", "nav"}.difference(df.columns):
        raise ValueError(f"Unexpected response shape for AMFI code {amfi_code}")

    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df = df.dropna(subset=["date", "nav"]).sort_values("date")
    return df


def main() -> None:
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"NAV ETL started at {run_time}")

    summary_rows = []
    for name, code in SCHEMES.items():
        try:
            nav_df = fetch_nav_history(code)
            output_path = RAW_DIR / f"{name}.csv"
            nav_df.to_csv(output_path, index=False)

            latest_row = nav_df.iloc[-1]
            summary_rows.append(
                {
                    "scheme": name,
                    "amfi_code": code,
                    "latest_date": latest_row["date"].strftime("%Y-%m-%d"),
                    "latest_nav": float(latest_row["nav"]),
                }
            )
            print(f"Saved {output_path.name} with {len(nav_df)} rows")
        except Exception as exc:
            print(f"Failed for {name}: {exc}")

    if summary_rows:
        summary_df = pd.DataFrame(summary_rows)
        summary_df.to_csv(RAW_DIR / "nav_fetch_summary.csv", index=False)
        print("Saved nav_fetch_summary.csv")

    print("NAV ETL completed")


if __name__ == "__main__":
    main()