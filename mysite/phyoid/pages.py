from flask import Blueprint, request, jsonify
import sqlite3
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


bp = Blueprint("phyoid", __name__, template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect("phyoid.db")
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn


conn = get_db_connection()
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS userDB(
    userID INTEGER PRIMARY KEY,
    name VARCHAR(100),
    passw VARCHAR(60),
    sets TEXT,
    grades TEXT
)''')
conn.commit()


@bp.route('/api/phyoid/register',methods=['POST'])
def add_user():
    new_user = request.json
    if not new_user:
        return jsonify({'error': 'Invalid input'}), 400

    name = new_user.get("name")
    passw = new_user.get("passw")
    hashpass = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
    cur.execute('INSERT INTO users (name, passw, sets, grades) VALUES (?, ?, ?, ?)', (name,hashpass,'[]','[]'))
    conn.commit()

    conn.close()

    access_token = create_access_token(identity=name)
    return jsonify(access_token=access_token), 201
