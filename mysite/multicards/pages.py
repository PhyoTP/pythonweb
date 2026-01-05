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
    and_tags = request.args.get('and_tags')  # comma-separated list: e.g. ?and_tags=math,physics
    or_tags = request.args.get('or_tags')    # comma-separated list: e.g. ?or_tags=chemistry,biology

    query = Setable.query.with_entities(
        Setable.id,
        Setable.name,
        Setable.creator,
        Setable.cardcount,
        Setable.tags
    )

    # --- Filtering logic ---
    if and_tags:
        and_tags_list = [t.strip() for t in and_tags.split(',') if t.strip()]
        # Check that all of these tags are contained in the tags column
        query = query.filter(Setable.tags.contains(and_tags_list))

    if or_tags:
        or_tags_list = [t.strip() for t in or_tags.split(',') if t.strip()]
        # Check that at least one overlaps
        query = query.filter(Setable.tags.overlap(or_tags_list))

    # --- Execute query ---
    sets_table = query.all()

    # --- Format response ---
    sets_list = [
        {
            "id": s.id,
            "name": s.name,
            "creator": s.creator,
            "isPublic": True,
            "cardCount": s.cardcount,
            "tags": s.tags
        } for s in sets_table
    ]
    
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
        "isPublic": True,
        "cardCount": fetched_set.cardcount,
        "tags": fetched_set.tags
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
        cardcount=len(new_set["cards"]),
        tags=new_set.get("tags", [])
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
            existing_set.cardcount = len(updated_set['cards'])
            existing_set.tags = updated_set.get('tags', [])
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

# admin
@bp.route('/multicards/admin/sets/delete', methods=['DELETE'])
@jwt_required()
def delete_set_admin():
    current_user = get_jwt_identity()
    if current_user != "PhyoTP":
        return jsonify({'msg': 'Forbidden'}), 403
    ids = request.args.get('ids')
    ids = ids.split(',')
    invalid_ids = []
    for id in ids:
        existing_set = Setable.query.get(id)

        if existing_set:
            db.session.delete(existing_set)
            db.session.commit()
        else:
            invalid_ids.append(id)
    if invalid_ids:
        return jsonify({'msg': 'Invalid IDs', 'invalid_ids': invalid_ids}), 400
    else:
        return '', 204

@bp.route('/multicards/admin/sets/recount', methods=['POST'])
@jwt_required()
def recount_sets():
    current_user = get_jwt_identity()
    if current_user != "PhyoTP":
        return jsonify({'msg': 'Forbidden'}), 403
    sets_table = Setable.query.all()
    for s in sets_table:
        s.cardcount = len(s.cards)
    db.session.commit()
    return '', 204