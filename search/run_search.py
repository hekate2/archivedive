import pyterrier as pt # type: ignore
import pandas as pd # type: ignore
import sqlite3
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# print(dir_path + "\data\sites.db")
conn = sqlite3.connect(dir_path + "\data\sites.db")

if not pt.java.started():
  pt.java.set_java_home("C:/Program Files/Java/jdk-23") # TODO: Figure out why it's not working when I add to path.
  pt.init()

df = pd.read_sql_query("""
    SELECT
        id AS docno,
        tags || ' ' || title || ' ' || summary AS text
    FROM sites
  """, conn, dtype={'docno': 'string'})

dir_path = os.path.dirname(os.path.realpath(__file__))
index_path = os.path.join(dir_path, "index")
indexer = pt.IterDictIndexer(index_path, overwrite=True)

index_ref = indexer.index(df.to_dict(orient="records"))

searcher = pt.terrier.Retriever(index_ref, wmodel="BM25")

conn.close()

def search_for_query(query):
  results = searcher.search(query)

  return results.to_dict(orient="records")