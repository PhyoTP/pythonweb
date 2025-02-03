from multiliterator.MultiLiterator.burm import convertToEng, convertToJap
from flask import Blueprint, request, render_template, jsonify

bp = Blueprint("multiliterator", __name__, template_folder='templates')

@bp.route('/multiliterator/burm/english', methods=['POST', 'GET'])
def convert_to_eng():
    if request.method == 'GET':
        return render_template("pages/burm/english.html")

    data = request.get_json(silent=True)  # Avoid error if request.json is None
    text = data.get("text") if data else None
    
    if not text:
        return jsonify({"error": "Missing text parameter"}), 400

    return jsonify({"output": convertToEng(text)}), 200

@bp.route('/multiliterator/burm/japanese', methods=['POST', 'GET'])
def convert_to_jap():
    if request.method == 'GET':
        return render_template("pages/burm/japanese.html")

    data = request.get_json(silent=True)  
    text = data.get("text") if data else None
    
    if not text:
        return jsonify({"error": "Missing text parameter"}), 400

    return jsonify({"output": convertToJap(text)}), 200

@bp.route('/multiliterator', methods=['GET'])
def home():
    return render_template("pages/multiliterator.html")
