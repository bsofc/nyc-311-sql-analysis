import sqlite3
import pandas as pd


print("NYC 311 Analysis for CV Portfolio")


conn = sqlite3.connect('nyc_311.db')

# convert date strings to SQLite dates with 
# SQLite's string manipulation

print("\n")
print("INSIGHT 1: Response Time by Borough (IN DAYS)")

query1 = """
SELECT 
    Borough,
    COUNT(*) as total_complaints,
    ROUND(AVG(
        julianday(
            substr("Closed Date", 7, 4) || '-' || 
            substr("Closed Date", 1, 2) || '-' || 
            substr("Closed Date", 4, 2) || ' ' ||
            substr("Closed Date", 12, 8)
        ) -
        julianday(
            substr("Created Date", 7, 4) || '-' || 
            substr("Created Date", 1, 2) || '-' || 
            substr("Created Date", 4, 2) || ' ' ||
            substr("Created Date", 12, 8)
        )
    ), 1) as avg_response_days
FROM nyc_311
WHERE Borough != 'Unspecified'
    AND "Closed Date" IS NOT NULL 
    AND "Created Date" IS NOT NULL
    AND "Closed Date" != ''
    AND "Created Date" != ''
GROUP BY Borough
ORDER BY avg_response_days DESC
"""
result1 = pd.read_sql(query1, conn)
print(result1.to_string(index=False))

print("\n")
print("INSIGHT 2: Most Common Complaint Types")


query2 = """
SELECT 
    "Complaint Type" as complaint_type,
    COUNT(*) as total,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM nyc_311), 1) as percentage
FROM nyc_311
GROUP BY "Complaint Type"
ORDER BY total DESC
LIMIT 10
"""
result2 = pd.read_sql(query2, conn)
print(result2.to_string(index=False))

print("\n")
print("INSIGHT 3: Noise Complaints by Borough")

query3 = """
SELECT 
    Borough,
    COUNT(*) as noise_complaints,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM nyc_311 WHERE "Complaint Type" LIKE '%Noise%'), 1) as pct_of_noise
FROM nyc_311
WHERE "Complaint Type" LIKE '%Noise%'
    AND Borough != 'Unspecified'
GROUP BY Borough
ORDER BY noise_complaints DESC
"""
result3 = pd.read_sql(query3, conn)
print(result3.to_string(index=False))

print("\n")
print("INSIGHT 4: Monthly Complaint Patterns (2025)")

query4 = """
SELECT 
    CASE strftime('%m', 
        substr("Created Date", 7, 4) || '-' || 
        substr("Created Date", 1, 2) || '-' || 
        substr("Created Date", 4, 2)
    )
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'
        WHEN '03' THEN 'March'
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
        WHEN '07' THEN 'July'
        WHEN '08' THEN 'August'
        WHEN '09' THEN 'September'
        WHEN '10' THEN 'October'
        WHEN '11' THEN 'November'
        WHEN '12' THEN 'December'
    END as month,
    COUNT(*) as total_complaints
FROM nyc_311
WHERE "Created Date" IS NOT NULL
GROUP BY month
ORDER BY total_complaints DESC
"""
result4 = pd.read_sql(query4, conn)
print(result4.to_string(index=False))

print("\n")
print("INSIGHT 5: Busiest Agencies")

query5 = """
SELECT 
    Agency,
    "Agency Name" as agency_name,
    COUNT(*) as complaints_handled,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM nyc_311), 1) as pct_of_total
FROM nyc_311
WHERE Agency IS NOT NULL
GROUP BY Agency
ORDER BY complaints_handled DESC
LIMIT 5
"""
result5 = pd.read_sql(query5, conn)
print(result5.to_string(index=False))

print("\n")
print("INSIGHT 6: Fastest vs Slowest Boroughs for Noise Complaints")

query6 = """
SELECT 
    Borough,
    COUNT(*) as noise_complaints,
    ROUND(AVG(
        julianday(
            substr("Closed Date", 7, 4) || '-' || 
            substr("Closed Date", 1, 2) || '-' || 
            substr("Closed Date", 4, 2)
        ) -
        julianday(
            substr("Created Date", 7, 4) || '-' || 
            substr("Created Date", 1, 2) || '-' || 
            substr("Created Date", 4, 2)
        )
    ), 1) as avg_response_days
FROM nyc_311
WHERE "Complaint Type" LIKE '%Noise%'
    AND Borough != 'Unspecified'
    AND "Closed Date" IS NOT NULL
GROUP BY Borough
ORDER BY avg_response_days DESC
"""
result6 = pd.read_sql(query6, conn)
print(result6.to_string(index=False))

print("\n")
print("INSIGHT 7: Top 5 ZIP Codes by Complaint Volume")

query7 = """
SELECT 
    "Incident Zip" as zip_code,
    COUNT(*) as total_complaints,
    Borough
FROM nyc_311
WHERE "Incident Zip" IS NOT NULL AND "Incident Zip" != ''
GROUP BY "Incident Zip"
ORDER BY total_complaints DESC
LIMIT 5
"""
result7 = pd.read_sql(query7, conn)
print(result7.to_string(index=False))

print("\n")
print("INSIGHT 8: Illegal Parking Hotspots (Top 5 ZIPs)")

query8 = """
SELECT 
    "Incident Zip" as zip_code,
    Borough,
    COUNT(*) as illegal_parking_complaints
FROM nyc_311
WHERE "Complaint Type" = 'Illegal Parking'
    AND Borough != 'Unspecified'
GROUP BY "Incident Zip"
ORDER BY illegal_parking_complaints DESC
LIMIT 5
"""
result8 = pd.read_sql(query8, conn)
print(result8.to_string(index=False))

conn.close()


