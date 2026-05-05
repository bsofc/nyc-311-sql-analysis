import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('nyc_311.db')

#Chart 1: Noise complaints by borough
query = """
SELECT Borough, COUNT(*) as complaints
FROM nyc_311
WHERE "Complaint Type" LIKE '%Noise%' AND Borough != 'Unspecified'
GROUP BY Borough
"""
df = pd.read_sql(query, conn)

plt.figure(figsize=(8, 5))
plt.bar(df['Borough'], df['complaints'], color='steelblue')
plt.title('Noise Complaints by Borough (Sept 2025)', fontsize=14)
plt.ylabel('Number of Complaints')
plt.xlabel('Borough')
for i, v in enumerate(df['complaints']):
    plt.text(i, v + 100, str(v), ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('noise_complaints_by_borough.png', dpi=150)

#Chart 2: Top 5 complaint types
query2 = """
SELECT "Complaint Type" as type, COUNT(*) as total
FROM nyc_311
GROUP BY type
ORDER BY total DESC
LIMIT 5
"""
df2 = pd.read_sql(query2, conn)

plt.figure(figsize=(10, 5))
plt.barh(df2['type'], df2['total'], color='coral')
plt.title('Top 5 Complaint Types (Sept 2025)', fontsize=14)
plt.xlabel('Number of Complaints')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('top_complaint_types.png', dpi=150)

conn.close()