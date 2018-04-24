from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db
#from forms import LoginForm
from .getfunc import getinfo
from models import User, ROLE_USER, ROLE_ADMIN
from models import Temp, NODATA



@app.route('/')
@app.route('/index')
def index():
    return render_template("temp.html",
        title = 'Home',
        result = getinfo())
