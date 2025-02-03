from flask import Blueprint, render_template, request, jsonify
import json
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import db, Setable

bp = Blueprint("multicards", __name__, template_folder='templates')

@bp.route("/")
def home():
    return render_template("pages/home.html")

@bp.route('/multicards/sets', methods=['GET'])
def get_sets():
    sets_table = Setable.query.with_entities(Setable.id, Setable.name, Setable.creator).all()
    sets_list = [{"id": s.id, "name": s.name, "creator": s.creator} for s in sets_table]
    return jsonify(sets_list), 200

@bp.route('/multicards/set/<uuid>', methods=['GET'])
def get_set(uuid):
    fetched_set = Setable.query.get(uuid)

    if fetched_set is None:
        return jsonify({'error': 'Set not found'}), 404

    fetched_dict = {
        "id": fetched_set.id,
        "name": fetched_set.name,
        "creator": fetched_set.creator,
        "cards": fetched_set.cards,
        "isPublic": fetched_set.ispublic
    }

    return jsonify(fetched_dict), 200

@bp.route('/multicards/sets', methods=['POST'])
def add_set():
    new_set = request.json
    set_entry = Setable(
        id=new_set["id"],
        name=new_set["name"],
        cards=json.dumps(new_set["cards"]),
        creator=new_set["creator"],
        ispublic=new_set["isPublic"]
    )
    db.session.add(set_entry)
    db.session.commit()

    return jsonify(new_set), 201

@bp.route('/multicards/sets/update/<setID>', methods=['PUT'])
@jwt_required()
def update_set(setID):
    current_user = get_jwt_identity()
    updated_set = request.json
    existing_set = Setable.query.get(setID)

    if existing_set:
        if existing_set.creator == current_user:
            existing_set.name = updated_set['name']
            existing_set.cards = json.dumps(updated_set['cards'])
            db.session.commit()
            return jsonify({'msg': 'Updated Successfully'}), 200
        else:
            return jsonify({'msg': 'Forbidden'}), 403
    else:
        return jsonify({'msg': 'Not Found'}), 404

@bp.route('/multicards/sets/delete/<setID>', methods=['DELETE'])
@jwt_required()
def delete_set(setID):
    current_user = get_jwt_identity()
    existing_set = Setable.query.get(setID)

    if existing_set:
        if existing_set.creator == current_user:
            db.session.delete(existing_set)
            db.session.commit()
            return '', 204
        else:
            return jsonify({'msg': 'Forbidden'}), 403
    else:
        return jsonify({'msg': 'Not Found'}), 404
@bp.route('/multicards/user/sets_rename', methods=['PUT'])
@jwt_required()
def rename_user_sets():
    current_user = get_jwt_identity()
    Setable.query.filter_by(creator=current_user).update({Setable.creator: None})
    db.session.commit()
    return '', 204

@bp.route('/multicards/user/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user = get_jwt_identity()
    Setable.query.filter_by(creator=current_user).delete()
    db.session.commit()
    return '', 204