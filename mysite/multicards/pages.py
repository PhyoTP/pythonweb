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
conn = get_db_connection()
cur = conn.cursor()
cur.execute('''ALTER TABLE setable
ADD COLUMN isPublic INTEGER''')
conn.commit()
conn.close()
@bp.route('/api/multicards/sets', methods=['GET'])
def get_sets():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM setable')
    sets_table = cur.fetchall()
    conn.commit()
    conn.close()

    # Convert the fetched rows to a list of dictionaries
    sets_list = [dict(row) for row in sets_table]
    for i in sets_list:
        i["cards"] = json.loads(i["cards"])  # Correctly load the JSON string into a Python object
        i["isPublic"] = bool(i["isPublic"])

    return jsonify(sets_list), 200

@bp.route('/api/multicards/sets', methods=['POST'])
def add_set():
    conn = get_db_connection()
    cur = conn.cursor()
    new_set = request.json

    cur.execute('INSERT INTO setable (id, name, cards, creator, isPublic) VALUES (?, ?, ?, ?, ?)', (new_set["id"], new_set["name"], json.dumps(new_set["cards"]), new_set["creator"], new_set["isPublic"]))
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

    cur.execute('SELECT * FROM setable WHERE id = ?', (setID,))
    old_set = cur.fetchone()
    conn.commit()
    if old_set:
        if old_set['creator'] == current_user:
            cur.execute('UPDATE setable SET name = ?, cards = ? WHERE id = ?', (updated_set['name'], json.dumps(updated_set['cards']), setID))
            conn.close()
            return jsonify({'msg': 'Updated Successfully'}), 200
        else:
            conn.close()
            return jsonify({'msg':'Forbidden'}), 403
    else:
        conn.close()
        return jsonify({'msg':'Not Found'}), 404
@bp.route('/api/multicards/sets/delete/<setID>',methods=['DELETE'])
@jwt_required()
def delete_set(setID):
    current_user = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM set WHERE id = ?', (setID,))
    old_set = cur.fetchone()
    conn.commit()
    if old_set:
        if old_set['creator'] == current_user:
            cur.execute('DELETE FROM setable WHERE setID = ?', (setID,))
            conn.close()
            return '', 204
        else:
            conn.close()
            return jsonify({'msg':'Forbidden'}), 403
    else:
        conn.close()
        return jsonify({'msg':'Not Found'}), 404
