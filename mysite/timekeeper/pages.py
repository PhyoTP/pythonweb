from flask import Blueprint, request, jsonify
from timekeeper.timekeeper import app as slack_app
from slack_bolt.adapter.flask import SlackRequestHandler

bp = Blueprint('timekeeper', __name__)

handler = SlackRequestHandler(slack_app)

@bp.route('/timekeeper', methods=['POST'])
def timekeeper():
    return handler.handle(request)
