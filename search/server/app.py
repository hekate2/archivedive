from flask import Flask, request, send_from_directory
from run_search import search_for_query
import sqlite3
import os
from flask_cors import CORS
from waitress import serve

dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(dir_path, "..", "data", "sites.db")
build_folder = os.path.join(dir_path, "..", "build")

app = Flask(__name__, static_folder=build_folder, static_url_path="/")
cors = CORS(app) # allow CORS for all domains on all routes.

app.config['CORS_HEADERS'] = 'Content-Type'

def get_int_arg(val, default):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

@app.route("/")
def serve_root():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/search")
def serve_search():
    return send_from_directory(app.static_folder, "search.html")

@app.route("/donate")
def serve_donate():
    return send_from_directory(app.static_folder, "donate.html")

@app.route("/about")
def serve_about():
    return send_from_directory(app.static_folder, "about.html")

@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory(app.static_folder, 'not_found.html'), 404

@app.route("/test")
def hello_world():
    return "Hello, World!", 200

@app.route("/api/lucky")
def lucky_route():
    try:
        random_q = "SELECT url FROM sites ORDER BY RANDOM() LIMIT 1;"

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(random_q)
            res = cursor.fetchall()

        return {"type": "success", "url": res[0][0]}
    except Exception as e:
        return {"type": "error", "message": str(e)}, 400
    

@app.route("/api/search")
def search_route():
    query = request.args.get('q')
    start = get_int_arg(request.args.get('p'), 0)
    num_results = get_int_arg(request.args.get('num_results'), 10)

    if not query:
        return "Please provide a search query", 400

    search_results = search_for_query(query)  # Fetch all matching document IDs

    if not search_results:
        return {"results": [], "num_results": 0}

    # Apply pagination BEFORE fetching from the database
    paginated_results = search_results[(start * num_results):(start * num_results) + num_results]

    result_ids = [str(doc["docno"]) for doc in paginated_results]

    if not result_ids:
        return {"results": [], "start": start, "num_results": num_results}

    placeholders = ", ".join(["?"] * len(result_ids))
    sql = f"SELECT title, url, summary FROM sites WHERE id IN ({placeholders})"

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, result_ids)
        rows = cursor.fetchall()

    return {"type": "success", "results": rows, "num_results": len(search_results)}


# app.run(host='0.0.0.0', port=5000)
serve(app, host="0.0.0.0", port=5000)