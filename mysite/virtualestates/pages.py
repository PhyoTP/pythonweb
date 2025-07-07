from flask import Blueprint, request, render_template, jsonify
import json
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import db, UserDB
import os
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, 'estates.json')
bp = Blueprint("virtualestates", __name__, template_folder='templates')
with open(DATA_FILE, "r") as file:
    estates = json.load(file)

@bp.route('/virtualestates/length', methods=['GET'])
def get_estates_by_length():
    length = request.args.get('length', default=0, type=str)
    try:
        length = int(length)
        if length <= 64:
            return jsonify({
                key: value for key, value in estates.items() if len(key) == length
            }), 200
        else:
            return jsonify({"error": "Length must be at most 64"}), 400
    except ValueError:
        return jsonify({"error": "Length must be an integer"}), 400

@bp.route('/virtualestates/name', methods=['GET'])
def get_estate_by_name():
    name = request.args.get('name', default='', type=str)
    if name in estates:
        return jsonify({name: estates[name]}), 200
    else:
        return jsonify({"error": "Estate not found"}), 404
@bp.route('/virtualestates/create', methods=['POST'])
@jwt_required()
def create_estate(name):
    data = request.json
    current_user = get_jwt_identity()
    if name in estates:
        return jsonify({"error": "Estate already exists"}), 400

    if not name.isalnum() or len(name) > 64 or not name.isascii():
        return jsonify({"error": "Invalid estate name. Must be alphanumeric ASCII and up to 64 characters."}), 400
    if data["creator"] != current_user:
        return jsonify({"error": "Username does not match creator"}), 400
    estates[name] = data
    with open(DATA_FILE, "w") as f:
        json.dump(estates, f, indent=4)
    user = UserDB.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.estates is None:
        user.estates = [name]
    else:
        user.estates = user.estates + [name]

    db.session.commit()
    return jsonify({"message": "Estate created successfully"}), 201