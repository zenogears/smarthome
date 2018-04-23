from app import app
from flask import render_template
from .getfunc import getinfo


@app.route('/')
@app.route('/index')
def index():
    return render_template("temp.html",
        title = 'Home',
        result = getinfo())
