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

    if not query:
      return "Please provide a search query", 400

    search = search_for_query(query)

    if len(search["docid"].values()) == 0:
       return []

    result_ids = [str(i) for i in search["docid"].values()]

    placeholders = " OR ".join(["id=?" for _ in result_ids])
    sql = f"SELECT title, url, summary FROM sites WHERE {placeholders}"

    print(result_ids)


    rows = []
    with sqlite3.connect(dir_path + "\\..\\data\\sites.db") as conn:
      cursor = conn.cursor()
      cursor.execute(sql, list(result_ids))
      rows = cursor.fetchall()

    return rows

app.run(host='0.0.0.0', port=5000)