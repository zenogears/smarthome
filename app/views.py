from app import app
from .getfunc import getinfo


@app.route('/')
@app.route('/index')
def index():
    return str(getinfo())
