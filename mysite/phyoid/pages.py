from flask import Blueprint, request, jsonify
import sqlite3
import json

bp = Blueprint("phyoid", __name__, template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect("phyoid.db")
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn


conn = get_db_connection()
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users(
    userID TEXT PRIMARY KEY,
    name VARCHAR(100),
    sets TEXT,
    grades TEXT
)''')
conn.commit()

@bp.route('/api/phyoid/<uuid>', methods=['GET'])
def get_user(uuid):
    cur.execute('SELECT * FROM users WHERE userID = ?', (uuid,))
    user = cur.fetchone()
    conn.commit()
    conn.close()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Convert the row to a dictionary
    user_dict = dict(user)
    user_dict["sets"] = json.loads(user_dict["sets"])
    user_dict["grades"] = json.loads(user_dict["grades"])

    return jsonify(user_dict)
@bp.route('/api/phyoid',methods=['POST'])
def add_user():
    new_user = request.json
    if not new_user:
        return jsonify({'error': 'Invalid input'}), 400


    cur.execute('INSERT INTO users (userID, name, sets, grades) VALUES (?, ?, ?, ?)', (
        new_user["userID"],
        new_user["name"],
        json.dumps(new_user["sets"]),
        json.dumps(new_user["grades"])
    ))
    conn.commit()

    conn.close()

    return jsonify({'message': 'User added successfully'}), 201
