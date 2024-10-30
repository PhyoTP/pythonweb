from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from multicards import pages as m
from phyoid import pages as p

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = ""
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "PATCH"])

# Register blueprints
app.register_blueprint(m.bp)
app.register_blueprint(p.bp)

if __name__ == '__main__':
    app.run(debug=True)
