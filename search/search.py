import pyterrier as pt # type: ignore
import pandas as pd # type: ignore
import sqlite3

conn = sqlite3.connect('data/sites.db')

if not pt.java.started():
  pt.java.set_java_home("C:/Program Files/Java/jdk-23") # TODO: Figure out why it's not working when I add to path.
  pt.init()

df = pd.read_sql_query("""
    SELECT
        id AS docno,
        tags || ' ' || title || ' ' || summary AS text
    FROM sites
  """, conn, dtype={'docno': 'string'})

# df = pd.DataFrame(documents)
indexer = pt.IterDictIndexer("C:/Users/wretc/Documents/Websites/archivedive/search/index", overwrite=True)
index_ref = indexer.index(df.to_dict(orient="records"))

searcher = pt.terrier.Retriever(index_ref, wmodel="BM25")

query = None

while query != "exit":
  query = input('Search term:')

  # Run the search
  results = searcher.search(query)
  print(f"Search results for query: '{query}'")
  print(results[['docno', 'score']])

conn.close()