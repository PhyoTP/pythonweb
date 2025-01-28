from flask import Flask
from flask_jwt_extended import JWTManager
from multicards import pages as m
from phyoid import pages as p
from stickynotes import pages as s
from models import db
from flask_cors import CORS
app = Flask(__name__)
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv("KEY")
passw = os.getenv("PASSW")

# Set up PostgreSQL URIs for multiple databases
app.config["SQLALCHEMY_BINDS"] = {
    "phyoid": "postgresql://phyotp:"+passw+"@hackclub.app/phyotp_phyoid",
    "multicards": "postgresql://phyotp:"+passw+"@hackclub.app/phyotp_multicards"
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = key

# Initialize SQLAlchemy and JWT Manager
db.init_app(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "PATCH"])

# Register blueprints
app.register_blueprint(m.bp)
app.register_blueprint(p.bp)
app.register_blueprint(s.bp)

if __name__ == '__main__':
    with app.app_context():
        # Create all tables for each bind
        db.create_all('phyoid')   # Create tables for the phyoid database
        db.create_all('multicards')  # Create tables for the multicards database
    app.run(host='0.0.0.0', port=6582, debug=False)
