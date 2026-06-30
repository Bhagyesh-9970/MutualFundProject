import os
import glob
import sqlite3
import pandas as pd


def find_csv_files(processed_dir="data/processed", raw_dir="data/raw"):
    processed = glob.glob(os.path.join(processed_dir, "*.csv"))
    raw = glob.glob(os.path.join(raw_dir, "*.csv"))

    # Use processed files preferentially
    files = {os.path.basename(p): p for p in raw}
    files.update({os.path.basename(p): p for p in processed})

    return files.values()


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    # Try to parse any column with 'date' in the name
    for col in df.columns:
        if "date" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass
    return df


def write_tables_to_sqlite(db_path="dashboard/bluestock_mf.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)

    csv_files = list(find_csv_files())
    if not csv_files:
        print("No CSV files found in data/processed or data/raw")
        return

    for path in csv_files:
        name = os.path.splitext(os.path.basename(path))[0]
        print(f"Loading {path} -> table `{name}`")
        try:
            df = pd.read_csv(path)
        except Exception as e:
            print(f"Failed to read {path}: {e}")
            continue

        df = parse_dates(df)

        # Normalize column names to safe sqlite names
        df.columns = [c.strip().replace(" ", "_") for c in df.columns]

        try:
            df.to_sql(name, conn, if_exists="replace", index=False)
            print(f"Wrote table `{name}` ({len(df)} rows)")
        except Exception as e:
            print(f"Failed to write table {name}: {e}")

        # Add helpful indexes for common join columns
        cur = conn.cursor()
        if "amfi_code" in df.columns:
            try:
                cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{name}_amfi_code ON {name} (amfi_code)")
            except Exception:
                pass
        # add indexes on any date-like column
        for col in df.columns:
            if "date" in col.lower():
                try:
                    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{name}_{col} ON {name} ({col})")
                except Exception:
                    pass

    conn.commit()
    conn.close()
    print(f"SQLite DB created at {db_path}")


if __name__ == "__main__":
    write_tables_to_sqlite()
