from flask import Blueprint, request, jsonify
app = bp = Blueprint('aasa', __name__)

@app.route('/apple-app-site-association', methods=['GET'])
def apple_app_site_association():
    data = {
        "applinks": {
            "apps": [],
            "details": [
                {
                    "appID": "YBKKM9K8UR.dev.phyotp.multicardsapp",
                    "paths": [ "/multicards/redirect/*" ]
                }
            ]
        }
    }
    response = jsonify(data)
    response.headers['Content-Type'] = 'application/json'
    return response
