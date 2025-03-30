# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserDB(db.Model):
    __tablename__ = 'users'  # Assuming you want the table name to be 'users'
    __bind_key__ = 'phyoid'  # Connects this model to the phyoid database
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    hashpass = db.Column(db.String(60), nullable=False)
    sets = db.Column(db.Text, nullable=False, default='[]')
    subjects = db.Column(db.Text, nullable=False, default='[]')
    verdi = db.Column(db.Text, nullable=False, default='{}')

class Setable(db.Model):
    __tablename__ = 'setable'  # Assuming you want the table name to be 'setable'
    __bind_key__ = 'multicards'  # Connects this model to the multicards database
    id = db.Column(db.String, primary_key=True)  # Adjust as needed for your ID type
    name = db.Column(db.String, nullable=False)
    cards = db.Column(db.Text, nullable=False, default='[]')
    creator = db.Column(db.String, nullable=False)
    ispublic = db.Column(db.Boolean, default=False)
