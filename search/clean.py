import re
import sqlite3

db_path = 'data/sites.db'

def main():
  clean_up_sites(db_path)

# Cleans up duplicates of archived urls
def clean_up_sites(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    archive_url_pattern = re.compile(r"https://web.archive.org/web/\d{14}if_/(.*)")

    cursor.execute("SELECT DISTINCT url FROM sites")
    rows = cursor.fetchall()

    seen_urls = set()

    for row in rows:
        url = row[0]
        match = archive_url_pattern.match(url)
        if match:
            original_url = match.group(1)
            if original_url not in seen_urls:
                seen_urls.add(original_url)
            else:
                cursor.execute("DELETE FROM sites WHERE url = ?", (url,))
                conn.commit()

    conn.close()


if __name__=="__main__":
  main()