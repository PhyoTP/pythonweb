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
    username VARCHAR(100),
    hashpass VARCHAR(60),
    sets TEXT,
    subjects TEXT
)''')
conn.commit()
conn.close()

@bp.route('/api/phyoid/register', methods=['POST'])
def add_user():
    conn = get_db_connection()
    cur = conn.cursor()

    new_user = request.json
    if not new_user:
        conn.close()
        return jsonify({'error': 'Invalid input'}), 400

    username = new_user.get("username")
    password = new_user.get("password")

    if not username or not password:
        conn.close()
        return jsonify({'error': 'Missing username or password'}), 400

    # Check if the username already exists
    cur.execute('SELECT username FROM userDB WHERE username = ?', (username,))
    existing_user = cur.fetchone()

    if existing_user:
        conn.commit()
        conn.close()
        return jsonify({'error': 'Username already exists'}), 409

    # Proceed with user registration
    hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cur.execute('INSERT INTO userDB (username, hashpass, sets, subjects) VALUES (?, ?, ?, ?)',
                (username, hashpass, '[]', '[]'))
    conn.commit()
    conn.close()

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 201

@bp.route('/api/phyoid/login', methods=['POST'])
def check_user():
    user = request.json
    if not user:
        return jsonify({'error': 'Invalid input'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    username = user.get("username")
    password = user.get("password")

    cur.execute('SELECT * FROM userDB WHERE username = ?', (username,))
    user_data = cur.fetchone()
    conn.commit()
    conn.close()
    if not user_data:
        return jsonify({'error': 'User not found'}), 404
    if bcrypt.checkpw(password.encode('utf-8'), user_data["hashpass"]):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad credentials"}), 401
@bp.route('/api/phyoid/update/<data>', methods=['PATCH'])
@jwt_required()
def update_user(data):
    allowed_data = {'username', 'sets', 'subjects'}

    if data not in allowed_data:
        return jsonify({'error': 'Invalid column'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    current_user = get_jwt_identity()
    new = request.json
    new_data = new.get(data)
    cur.execute(f'UPDATE userDB SET {data} = ? WHERE username = ?', (json.dumps(new_data), current_user))
    conn.commit()
    conn.close()

    return jsonify({"msg": "User data updated successfully"}), 200
@bp.route('/api/phyoid/userdata', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()  # Get the username from the JWT token
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch the user data based on the username
    cur.execute('SELECT * FROM userDB WHERE username = ?', (current_user,))
    user_data = cur.fetchone()

    conn.commit()
    conn.close()

    if not user_data:
        return jsonify({'error': 'User not found'}), 404

    # Convert the user_data to a dictionary and return it
    user_info = {
        "username": user_data["username"],
        "sets": json.loads(user_data["sets"]),
        "subjects": json.loads(user_data["subjects"])
    }

    return jsonify(user_info), 200