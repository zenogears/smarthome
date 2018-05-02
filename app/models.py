import jwt
import datetime
from time import time

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, current_user
import flask_whooshalchemy as whooshalchemy

from hashlib import md5

from app import app, db, login

ROLE_USER = 0
ROLE_ADMIN = 1
NODATA = 0
NOPIC = 'no picture'

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
    my_raspberry = db.Column(db.String(140))
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

    def follow(self, username):
        if not self.is_following(username):
            self.followed.append(username)
            return self

    def unfollow(self, username):
        if self.is_following(username):
            self.followed.remove(username)
            return self

    def is_following(self, username):
        return self.followed.filter(followers.c.followed_id == username.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

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
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)



class RasModels(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    mname = db.Column(db.String(24), index = True)
    mpins = db.Column(db.Integer, index = True)

    def __repr__(self):
        return '<RasModels %r>' % (self.mname)

class Raspb3BPins(db.Model): #User
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(24))
    number = db.Column(db.String(8))
    pin_info = db.Column(db.String(140))
    connected = db.relationship('Sensors', backref = 'conpin')

    def __repr__(self):
        return '<Raspb3BPins %r>' % (self.id)

    # def connected(self,sensor_id):
    #     #self.followed.append(username)
    #     #return self
    #     return True

class Sensorsdb(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140), index = True)
    about = db.Column(db.String(140), index = True)
    pic = db.Column(db.String(256))

    def __repr__(self):
        return '<Sensor %r>' % (self.name)

class Sensors(db.Model): #Post
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    raspin_id = db.Column(db.Integer, db.ForeignKey('raspb3_b_pins.id'))

    def __repr__(self):
        return '<Sensors %r>' % (self.name)

whooshalchemy.whoosh_index(app, Post)