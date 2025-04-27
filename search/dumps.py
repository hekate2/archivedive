import sqlite3
import csv

db_filename = "data/sites.db"
csv_filename = "data/sites.csv"

conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# make tbl
cursor.execute('''
CREATE TABLE IF NOT EXISTS "sites" (
    "id" INTEGER NOT NULL,
    "title" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "summary" TEXT,
    "tags" NUMERIC NOT NULL,
    "archived_on" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "visits" INTEGER NOT NULL DEFAULT 0,
    "display_count" INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY("id" AUTOINCREMENT)
);
''')

# dump data from csv
with open(csv_filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO sites (title, url, summary, tags, archived_on, visits, display_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['title'],
            row['url'],
            row.get('summary', None),
            row['tags'],
            row.get('archived_on', None),
            row.get('visits', 0),
            row.get('display_count', 0)
        ))

conn.commit()
conn.close()

print(f"Data from {csv_filename} has been imported into {db_filename}.")
