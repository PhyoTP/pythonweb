# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserDB(db.Model):
    __tablename__ = 'users'  # Assuming you want the table name to be 'users'
    __bind_key__ = 'phyoid'  # Connects this model to the phyoid database
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    hashpass = db.Column(db.String(60), nullable=False)
    badges = db.Column(db.ARRAY(db.String(50)), nullable=False, default=[])
    sets = db.Column(db.Text, nullable=False, default='[]')
    subjects = db.Column(db.Text, nullable=False, default='[]')
    verdi = db.Column(db.Text, nullable=False, default='{}')
    email = db.Column(db.Text)
    __table_args__ = (
        db.CheckConstraint(
            r"email ~ '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'",
            name='email_format_check'
        ),
    )

class Setable(db.Model):
    __tablename__ = 'setable'  # Assuming you want the table name to be 'setable'
    __bind_key__ = 'multicards'  # Connects this model to the multicards database
    id = db.Column(db.String, primary_key=True)  # Adjust as needed for your ID type
    name = db.Column(db.String, nullable=False)
    cards = db.Column(db.Text, nullable=False, default='[]')
    creator = db.Column(db.String, nullable=False)
    cardcount = db.Column(db.Integer, nullable=False, default=0)

class Otps(db.Model):
    __tablename__ = 'otps'  # Assuming you want the table name to be 'otps'
    __bind_key__ = 'phyoid'  # Connects this model to the phyoid database
    id = db.Column(db.Integer, primary_key=True)
    hashcode = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    type = db.Column(db.String(10), nullable=False)  # 'email' or 'sms'