import sqlite3
import pandas as pd

conn = sqlite3.connect("bluestock_mf.db")

queries = {

"Top 5 Funds by AUM":
"""
SELECT scheme_name, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5
""",

"Transactions by State":
"""
SELECT state, COUNT(*) total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC
"""

}

for title, query in queries.items():

    print("\n", "="*50)
    print(title)
    print("="*50)

    df = pd.read_sql(query, conn)

    print(df)

conn.close()