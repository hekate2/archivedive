from flask import Flask, request
import sys
from run_search import search_for_query
import sqlite3
import os
from flask_cors import CORS, cross_origin

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello_world():
    return "Hello, World!", 200

@app.route("/search")
def search_route():
    query = request.args.get('q')
    start = int(request.args.get('start', 0))  # Default: start at result 0
    num_results = int(request.args.get('num_results', 10))  # Default: return 10 results

    if not query:
        return "Please provide a search query", 400

    search_results = search_for_query(query)  # Fetch all matching document IDs

    if not search_results:
        return {"results": [], "start": start, "num_results": num_results}

    print(search_results)
    print(start)
    print(num_results)
    # Apply pagination BEFORE fetching from the database
    paginated_results = search_results[start:start + num_results]

    result_ids = [str(doc["docno"]) for doc in paginated_results]

    if not result_ids:
        return {"results": [], "start": start, "num_results": num_results}

    placeholders = ", ".join(["?"] * len(result_ids))
    sql = f"SELECT title, url, summary FROM sites WHERE id IN ({placeholders})"

    with sqlite3.connect(dir_path + "\\..\\data\\sites.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, result_ids)
        rows = cursor.fetchall()

    return rows
    # return {"results": rows, "start": start, "num_results": num_results, "total_matches": len(search_results)}

# # TODO: pagination, and figure out what the heck is going on with the queries (why returning bad matches?)
# @app.route("/search")
# def search_route():
#     query = request.args.get('q')

#     if not query:
#       return "Please provide a search query", 400

#     search = search_for_query(query)

#     if len(search["docid"].values()) == 0:
#        return []

#     result_ids = [str(i) for i in search["docid"].values()]

#     placeholders = " OR ".join(["id=?" for _ in result_ids])
#     sql = f"SELECT title, url, summary FROM sites WHERE {placeholders}"

#     print(result_ids)


#     rows = []
#     with sqlite3.connect(dir_path + "\\..\\data\\sites.db") as conn:
#       cursor = conn.cursor()
#       cursor.execute(sql, list(result_ids))
#       rows = cursor.fetchall()

#     return rows

app.run(host='0.0.0.0', port=5000)