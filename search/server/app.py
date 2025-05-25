from flask import Flask, request
from run_search import search_for_query
import sqlite3
import os
from flask_cors import CORS
from waitress import serve

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.

app.config['CORS_HEADERS'] = 'Content-Type'

def get_int_arg(val, default):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

@app.route("/")
def hello_world():
    return "Hello, World!", 200

@app.route("/api/search")
def search_route():
    print(request.args.get('p'))
    query = request.args.get('q')
    start = get_int_arg(request.args.get('p'), 0)
    num_results = get_int_arg(request.args.get('num_results'), 10)

    if not query:
        return "Please provide a search query", 400

    search_results = search_for_query(query)  # Fetch all matching document IDs

    if not search_results:
        return {"results": [], "num_results": num_results}

    # Apply pagination BEFORE fetching from the database
    paginated_results = search_results[(start * num_results):(start * num_results) + num_results]

    result_ids = [str(doc["docno"]) for doc in paginated_results]

    if not result_ids:
        return {"results": [], "start": start, "num_results": num_results}

    placeholders = ", ".join(["?"] * len(result_ids))
    sql = f"SELECT title, url, summary FROM sites WHERE id IN ({placeholders})"

    print("HELLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(dir_path + "/../data/sites.db")

    with sqlite3.connect(dir_path + "/../data/sites.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, result_ids)
        rows = cursor.fetchall()

    return {"results": rows, "num_results": len(search_results)}


# app.run(host='0.0.0.0', port=5000)
serve(app, host="0.0.0.0", port=5000)