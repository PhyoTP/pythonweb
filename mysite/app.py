from flask import Flask
from flask_jwt_extended import JWTManager
import secrets

from multicards import pages as m
from phyoid import pages as p

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = secrets.token_hex()
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(m.bp)
app.register_blueprint(p.bp)

if __name__ == '__main__':
    app.run(debug=True)
