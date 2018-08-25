import os
basedir = os.path.abspath(os.path.dirname(__file__))
with open('/home/pi/mailpassword','r') as f:
    passphrase = f.read()

class Config(object):
    TEMPLATES_AUTO_RELOAD = True
    MAX_SEARCH_RESULTS = 50
    WHOOSH_BASE = os.path.join(basedir, 'search.db')
    POSTS_PER_PAGE = 10
    POSTS_PER_PAGE_USER = 5
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'smarthome.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    # slow database query threshold (in seconds)
    DATABASE_QUERY_TIMEOUT = 0.5
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MJiopnsdfvhpbupdsfiubnarjklebvf;jbf'
    LANGUAGES = ['ru', 'en']

    # email server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'zenogears.aka@gmail.com'
    MAIL_PASSWORD = passphrase

    # administrator list
    ADMINS = ['zenogears.aka@gmail.com']
