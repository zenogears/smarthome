from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from hashlib import md5
from app import db, login
import datetime

ROLE_USER = 0
ROLE_ADMIN = 1
NODATA = 0

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(64), index = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User', 
        secondary = followers, 
        primaryjoin = (followers.c.follower_id == id), 
        secondaryjoin = (followers.c.followed_id == id), 
        backref = db.backref('followers', lazy = 'dynamic'), 
        lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode('utf8')).hexdigest() + '?d=mm&s=' + str(size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    @staticmethod
    def make_unique_nickname(username):
        if User.query.filter_by(username = username).first() == None:
            return username
        version = 2
        while True:
            new_nickname = username + str(version)
            if User.query.filter_by(username = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

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

class Raspb3B(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(24), index = True)
    number = db.Column(db.String(8), index = True)
    pin_info = db.Column(db.String(140))


    def __repr__(self):
        return '<pin %r>' % (self.name)