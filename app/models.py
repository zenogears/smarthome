from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import datetime

ROLE_USER = 0
ROLE_ADMIN = 1
NODATA = 0

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(64), index = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Temp(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime(), default=datetime.datetime.utcnow, unique = True)
    temperature = db.Column(db.SmallInteger, default = NODATA)
    humidity = db.Column(db.SmallInteger, default = NODATA)

    def __repr__(self):
        return '<time {0}>'.format(self.time)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)