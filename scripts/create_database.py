import sqlite3

# Create database
conn = sqlite3.connect("bluestock_mf.db")

# Read schema
with open("sql/schema.sql", "r") as f:
    schema = f.read()

# Execute schema
conn.executescript(schema)

print("Database created successfully!")

conn.close()