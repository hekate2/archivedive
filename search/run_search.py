import pyterrier as pt # type: ignore
import pandas as pd # type: ignore
import sqlite3
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(dir_path, "data", "sites.db")

print("BD PATH: " + db_path)

# print(dir_path + "\data\sites.db")
conn = sqlite3.connect(db_path)

df = pd.read_sql_query("""
    SELECT
        id AS docno,
        tags || ' ' || title || ' ' || summary AS text
    FROM sites
  """, conn, dtype={'docno': 'string'})

# if not pt.java.started():
#   pt.java.set_java_home("/usr/lib/jvm/default-java")

dir_path = os.path.dirname(os.path.realpath(__file__))
index_path = os.path.join(dir_path, "index")
indexer = pt.IterDictIndexer(index_path, overwrite=True)

index_ref = indexer.index(df.to_dict(orient="records"))

searcher = pt.terrier.Retriever(index_ref, wmodel="BM25")

conn.close()

def search_for_query(query):
  results = searcher.search(query)

  return results.to_dict(orient="records")