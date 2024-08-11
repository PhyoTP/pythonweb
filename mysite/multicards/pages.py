from flask import Blueprint, render_template, request, jsonify
import sqlite3
import json

bp = Blueprint("pages", __name__, template_folder='templates')

@bp.route("/multicards")
def home():
    return render_template("pages/home.html")

def get_db_connection():
    conn = sqlite3.connect("multicards.db")
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS setstable(
        setID INTEGER PRIMARY KEY,
        name TEXT,
        cards TEXT,
        creator VARCHAR(100)
    )''')
    conn.commit()
    conn.close()

create_table()

@bp.route('/multicards/api', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM setstable')
    sets_table = cur.fetchall()
    conn.close()

    # Convert the fetched rows to a list of dictionaries
    sets_list = [dict(row) for row in sets_table]
    for i in sets_list:
        i["cards"] = json.loads(i["cards"])  # Correctly load the JSON string into a Python object

    return jsonify(sets_list)

@bp.route('/multicards/api', methods=['POST'])
def add_item():
    new_set = request.json

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO setstable (name, cards, creator) VALUES (?, ?, ?)', (new_set["name"], json.dumps(new_set["cards"]), new_set["creator"]))
    conn.commit()
    conn.close()

    return jsonify(new_set), 201
