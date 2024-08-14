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


conn = get_db_connection()
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS setstable(
    setID INTEGER PRIMARY KEY,
    name TEXT,
    cards TEXT,
    creator VARCHAR(100)
)''')
conn.commit()
cur.execute('''CREATE TABLE IF NOT EXISTS userbase(
    userID TEXT PRIMARY KEY,
    name VARCHAR(100)
)''')
conn.commit()


@bp.route('/api/multicards/sets', methods=['GET'])
def get_sets():
    cur.execute('SELECT * FROM setstable')
    sets_table = cur.fetchall()
    conn.close()

    # Convert the fetched rows to a list of dictionaries
    sets_list = [dict(row) for row in sets_table]
    for i in sets_list:
        i["cards"] = json.loads(i["cards"])  # Correctly load the JSON string into a Python object

    return jsonify(sets_list)

@bp.route('/api/multicards/sets', methods=['POST'])
def add_set():
    new_set = request.json

    cur.execute('INSERT INTO setstable (name, cards, creator) VALUES (?, ?, ?)', (new_set["name"], json.dumps(new_set["cards"]), new_set["creator"]))
    conn.commit()
    conn.close()

    return jsonify(new_set), 201

@bp.route('/api/multicards/user/<uuid>', methods=['GET'])
def get_user(uuid):
    cur.execute('SELECT * FROM userbase WHERE userID = ?', (uuid,))
    user = cur.fetchone()
    conn.close()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Convert the row to a dictionary
    user_dict = dict(user)

    return jsonify(user_dict)
@bp.route('/api/multicards/user',methods=['POST'])
def add_user():
    new_user = request.json
    if not new_user:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        uuid, username = list(new_user.items())[0]
    except ValueError:
        return jsonify({'error': 'Invalid format'}), 400


    # Insert the UUID and username into the users table
    try:
        cur.execute('INSERT INTO userbase (userID, name) VALUES (?, ?)', (uuid, username))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'User with this UUID already exists or username is not unique'}), 400

    conn.close()

    return jsonify({'message': 'User added successfully'}), 201
