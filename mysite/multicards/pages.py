from flask import Blueprint, render_template, request, jsonify
import sqlite3
import json

bp = Blueprint("multicards", __name__, template_folder='templates')

@bp.route("/multicards")
def home():
    return render_template("pages/home.html")

def get_db_connection():
    conn = sqlite3.connect("multicards.db")
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn


@bp.route('/api/multicards/sets', methods=['GET'])
def get_sets():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM setstable')
    sets_table = cur.fetchall()
    conn.commit()
    conn.close()

    # Convert the fetched rows to a list of dictionaries
    sets_list = [dict(row) for row in sets_table]
    for i in sets_list:
        i["cards"] = json.loads(i["cards"])  # Correctly load the JSON string into a Python object

    return jsonify(sets_list)

@bp.route('/api/multicards/sets', methods=['POST'])
def add_set():
    conn = get_db_connection()
    cur = conn.cursor()
    new_set = request.json

    cur.execute('INSERT INTO setstable (name, cards, creator) VALUES (?, ?, ?)', (new_set["name"], json.dumps(new_set["cards"]), new_set["creator"]))
    conn.commit()
    conn.close()

    return jsonify(new_set), 201

