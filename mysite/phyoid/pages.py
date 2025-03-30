from flask import Blueprint, request, jsonify
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import json
from models import db, UserDB
import requests

bp = Blueprint("phyoid", __name__)

@bp.route('/phyoid/register', methods=['POST'])
def add_user():
    new_user = request.json
    if not new_user:
        return jsonify({'error': 'Invalid input'}), 400

    username = new_user.get("username")
    password = new_user.get("password")

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    # Check if the username already exists
    if UserDB.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    # Proceed with user registration
    try:
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = UserDB(username=username, hashpass=hashpass)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 201


@bp.route('/phyoid/login', methods=['POST'])
def check_user():
    user = request.json
    if not user:
        return jsonify({'error': 'Invalid input'}), 400

    username = user.get("username")
    password = user.get("password")

    user_data = UserDB.query.filter_by(username=username).first()
    if not user_data:
        return jsonify({'error': 'User not found'}), 404

    try:
        # Attempt to verify the password
        if bcrypt.checkpw(password.encode('utf-8'), user_data.hashpass.encode('utf-8')):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Bad credentials"}), 401
    except ValueError as e:
        # Handle cases where salt is invalid, likely due to old format
        if "Invalid salt" in str(e):
            response = requests.post('https://phyotp.pythonanywhere.com/api/phyoid/login', json=user)
            return response.json(), response.status_code
        else:
            # Reraise if it's an unexpected error
            raise


@bp.route('/phyoid/update/<data>', methods=['PATCH'])
@jwt_required()
def update_user(data):
    allowed_data = {'sets', 'subjects', 'verdi'}
    if data not in allowed_data:
        return jsonify({'error': 'Invalid column'}), 400

    current_user = get_jwt_identity()
    new_data = request.json.get(data)
    if new_data is None:
        return jsonify({'error': 'Invalid input'}), 400

    user = UserDB.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    setattr(user, data, json.dumps(new_data))
    db.session.commit()

    return jsonify({"msg": "User data updated successfully"}), 200

@bp.route('/phyoid/userdata', methods=['GET'])
@jwt_required()
def get_all_user_data():
    current_user = get_jwt_identity()
    user_data = UserDB.query.filter_by(username=current_user).first()

    if not user_data:
        return jsonify({'error': 'User not found'}), 404

    user_info = {
        "username": user_data.username,
        "sets": user_data.sets,
        "subjects": user_data.subjects,
        "verdi": user_data.verdi
    }
    return jsonify(user_info), 200

@bp.route('/phyoid/userdata/<data>', methods=['GET'])
@jwt_required()
def get_user(data):
    allowed_data = {'sets', 'subjects','verdi'}
    if data not in allowed_data:
        return jsonify({'error': 'Invalid column'}), 400

    current_user = get_jwt_identity()
    user = UserDB.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Retrieve the data from the user object
    user_data = getattr(user, data)
    
    # Check if user_data is already a list (decoded from JSON)
    if isinstance(user_data, str):
        # If it’s a JSON string, decode it to a list
        user_data = json.loads(user_data)
    
    return jsonify(user_data), 200


@bp.route('/phyoid/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@bp.route('/phyoid/delete', methods=['POST'])
@jwt_required()
def delete():
    data = request.json
    if not data or 'password' not in data:
        return jsonify({'error': 'Invalid input, password is required'}), 400

    password = data.get('password')
    current_user = get_jwt_identity()
    user = UserDB.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        # Attempt to verify the password
        if bcrypt.checkpw(password.encode('utf-8'), user.hashpass.encode('utf-8')):
            db.session.delete(user)
            db.session.commit()
            return jsonify({"msg": "User deleted successfully"}), 200
        else:
            return jsonify({"msg": "Bad credentials"}), 401
    except ValueError as e:
        if "Invalid salt" in str(e):
            # Attempt external deletion for legacy salt format
            response = requests.post(
                'https://phyotp.pythonanywhere.com/api/phyoid/delete',
                json=data
            )
            if response.status_code == 200:
                db.session.delete(user)
                db.session.commit()
                return jsonify({"msg": "User deleted successfully"}), 200
            else:
                return jsonify({'error': 'External deletion failed', 'details': response.json()}), response.status_code
        else:
            raise

# admin

@bp.route('/phyoid/admin/resetPassword', methods=['POST'])
@jwt_required()
def admin_reset_password():
    admin = get_jwt_identity()
    if admin != "PhyoTP":
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid input, username and password are required'}), 400
    username = data.get('username')
    password = data.get('password')
    user = UserDB.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.hashpass = hashpass
        db.session.commit()
        return jsonify({"msg": "Password reset successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500