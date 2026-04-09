import sqlite3
from decouple import config

DATABASE_URL = config("DATABASE_URL",cast=str,default="./db.sqlite")
conn = sqlite3.connect(DATABASE_URL) # type: ignore

cur = conn.cursor()


track_info = cur.execute("PRAGMA table_info(InvoiceLine)");
print("#" * 20)
print(*track_info, sep="\n")
print("#" * 20)

# Top 10 best-selling tracks
best_selling_tracks = cur.execute("" \
"""
SELECT 
    COUNT(tr.Name) AS n_distinct_names, 
    lnl.Quantity,
    tr.Name,
    ROUND(tr.UnitPrice * COUNT(tr.Name), 2) AS total_price
FROM Track tr
INNER JOIN InvoiceLine lnl ON tr.TrackId = lnl.TrackId
GROUP BY tr.Name
ORDER BY n_distinct_names DESC
LIMIT 10
""")
print(*best_selling_tracks, sep="\n")
cur.close()
