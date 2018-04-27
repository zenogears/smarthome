#!/usr/bin/python
import os
import unittest


from app import app, db
from config import basedir
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(username = 'john', email = 'john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(username = 'john', email = 'john@example.com')
        db.session.add(u)
        db.session.commit()
        username = User.make_unique_nickname('john')
        assert username != 'john'
        u = User(username = username, email = 'susan@example.com')
        db.session.add(u)
        db.session.commit()
        username2 = User.make_unique_nickname('john')
        assert username2 != 'john'
        assert username2 != username

    def test_follow(self):
        u1 = User(username = 'john', email = 'john@example.com')
        u2 = User(username = 'susan', email = 'susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) == None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) == None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().username == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().username == 'john'
        u = u1.unfollow(u2)
        assert u != None
        db.session.add(u)
        db.session.commit()
        assert u1.is_following(u2) == False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

if __name__ == '__main__':
    unittest.main()
