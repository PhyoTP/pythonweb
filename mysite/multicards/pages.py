from flask import Blueprint, render_template, request, jsonify
import sqlite3
import json
from flask_jwt_extended import get_jwt_identity, jwt_required

bp = Blueprint("multicards", __name__, template_folder='templates')

@bp.route("/multicards")
def home():
    return render_template("pages/home.html")

def get_db_connection():
    conn = sqlite3.connect("multicards.db")
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

# conn = get_db_connection()
# cur = conn.cursor()
# cur.execute('''CREATE TABLE IF NOT EXISTS setsdb(
#     setID VARCHAR(36) PRIMARY KEY,
#     name TEXT,
#     cards TEXT,
#     creator VARCHAR(100)
# )''')
# cur.execute('update setsdb set setID = "6cc7e8fe-2438-4f22-99f1-03ad6d64c5bb" where name = "Acid/base reactions"')
# conn.commit()
# conn.close()
@bp.route('/api/multicards/sets', methods=['GET'])
def get_sets():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM setsdb')
    sets_table = cur.fetchall()
    conn.commit()
    conn.close()

    # Convert the fetched rows to a list of dictionaries
    sets_list = [dict(row) for row in sets_table]
    for i in sets_list:
        i["cards"] = json.loads(i["cards"])  # Correctly load the JSON string into a Python object

    return jsonify(sets_list), 200

@bp.route('/api/multicards/sets', methods=['POST'])
def add_set():
    conn = get_db_connection()
    cur = conn.cursor()
    new_set = request.json

    cur.execute('INSERT INTO setsdb (name, cards, creator) VALUES (?, ?, ?)', (new_set["name"], json.dumps(new_set["cards"]), new_set["creator"]))
    conn.commit()
    conn.close()

    return jsonify(new_set), 201
@bp.route('/api/multicards/sets/update/<setID>',methods=['PUT'])
@jwt_required()
def update_set(setID):
    current_user = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    updated_set = request.json

    cur.execute('SELECT * FROM setsdb WHERE setID = ?', (setID,))
    old_set = cur.fetchone()
    conn.commit()
    if old_set:
        if old_set['creator'] == current_user:
            cur.execute('UPDATE setsdb SET name = ?, cards = ? WHERE setID = ?', (updated_set['name'], json.dumps(updated_set['cards']), setID))
            conn.close()
            return jsonify({'msg': 'Updated Successfully'}), 200
        else:
            conn.close()
            return jsonify({'msg':'Forbidden'}), 403
    else:
        conn.close()
        return jsonify({'msg':'Not Found'}), 404
