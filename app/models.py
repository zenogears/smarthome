from app import db
import datetime

ROLE_USER = 0
ROLE_ADMIN = 1
NODATA = 0

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(64), index = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

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