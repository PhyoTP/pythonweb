from flask import Blueprint, Response, request, jsonify
from notesverse.model import Subject

bp = Blueprint('notesverse', __name__)

@bp.route("/notesverse/make_graph", methods=["POST"])
def graph():
    data = request.json
    name = data.get("name", "Graph")
    text = data.get("text", "")

    subject = Subject(name)
    subject.convert_string(text)

    return Response(subject.make_graph(), mimetype="text/html")
@bp.route("/notesverse/get_topics", methods=["POST"])
def get_topics():
    data = request.json
    name = data.get("name", "Graph")
    text = data.get("text", "")

    subject = Subject(name)
    subject.convert_string(text)
    topics_dict = {name: topic.__dict__ for name, topic in subject.topics.items()}
    return jsonify(topics_dict), 200
if __name__ == "__main__":
    bp.run(debug=True)
