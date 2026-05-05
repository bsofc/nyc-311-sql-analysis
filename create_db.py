import sqlite3
import pandas as pd
import os


print("NYC 311 SQLite Database Creator")


csv_file = "nyc_311_sample.csv"

#check if file excists 
if not os.path.exists(csv_file):
    print(f"\n Error: Cannot find '{csv_file}'")
    exit(1)

# load CSV file
try:
    df = pd.read_csv(csv_file)
except Exception as e:
    exit(1)

# create SQLite database
db_file = "nyc_311.db"
conn = sqlite3.connect(db_file)

# save to SQLite
df.to_sql('nyc_311', conn, if_exists='replace', index=False)
# some stats 
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM nyc_311")
total_rows = cursor.fetchone()[0]
cursor.execute("PRAGMA table_info(nyc_311)")
columns = cursor.fetchall()

print(f"\n DB:")
print(f" Nb rows: {total_rows:,}")
print(f" Nb columns: {len(columns)}")
print(f" 5 columns: {', '.join([col[1] for col in columns[:5]])}")

# col names
print(f"\n column names:")
for i, col in enumerate(columns[:10]):  
    print(f"   {i+1}. {col[1]}")
if len(columns) > 10:
    print(f"   ... and {len(columns)-10} more")

conn.close()
