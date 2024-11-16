import pyterrier as pt # type: ignore
import pandas as pd # type: ignore

if not pt.started():
  pt.java.set_java_home("C:\Program Files\Java\jdk-23") # TODO: Figure out why it's not working when I add to path.
  pt.init()

# Sample documents
documents = [
    {'docno': '1', 'text': 'PyTerrier is a Python library for information retrieval.'},
    {'docno': '2', 'text': 'PyTerrier makes it easy to experiment with search engines.'},
    {'docno': '3', 'text': 'Information retrieval is a core task in many search engines.'},
    {'docno': '4', 'text': 'Learning about PyTerrier is fun and informative.'},
    {'docno': '5', 'text': 'This document is about machine learning and information retrieval.'}
]

df = pd.DataFrame(documents)
indexer = pt.IterDictIndexer("C:/Users/wretc/Documents/Websites/archivedive/search/index", overwrite=True)
index_ref = indexer.index(df.to_dict(orient="records"))

searcher = pt.terrier.Retriever(index_ref, wmodel="BM25")

query = "library"

# Run the search
results = searcher.transform(query)

print(f"Search results for query: '{query}'")
print(results[['docno', 'score']])