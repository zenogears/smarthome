import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'smarthome.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MJiopnsdfvhpbupdsfiubnarjklebvf;jbf'
    # mail server settings
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    # administrator list
    ADMINS = ['you@example.com']