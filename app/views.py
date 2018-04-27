#! -*- coding: utf8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from werkzeug.urls import url_parse
from app import app, db, login

from datetime import datetime

import plotly
import pandas as pd
import numpy as np
import json

from app.models import User, ROLE_USER, ROLE_ADMIN
from app.models import Temp, NODATA

from app.forms import LoginForm, RegistrationForm, EditForm

from app.getfunc import getinfo, getgraphinfo

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit() and form.invite.data == 'mwsfnklnvaklerklavbreb':
        username = User.make_unique_nickname(form.username.data)
        user = User(username=username, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.username)
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('usersettings',username=current_user.username))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html',
        form = form)

@app.errorhandler(401)
def page_not_found(error):
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main page')

@app.route('/rasp')
def rasp():
    return render_template('rsettings.html', title='Raspberry Pi config page')

@app.route('/user/<username>')
@login_required
def usersettings(username):
    
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': u'Сегодня была хорошая погода.' },
        { 'author': user, 'body': u'Температура на датчике просто замечательная.' }
    ]
    return render_template('usersettings.html',
        username = user,
        posts = posts,
        title='Settings page')

@app.route('/temp')
@login_required
def temp():
    return render_template("temp.html",
        title = 'Home',
        username = User.query.get('id'),
        result = getinfo())

@app.route('/tempgrapth')
@login_required
def tempgrapth():
    graphs = [
        dict(
                data = [
                    dict(
                                y = getgraphinfo()['x'],
                                x = [s for s in range(0,len(getgraphinfo()['y']))],
                                type='scatter'
                        )
                ],
                layout=dict(title='Temperature')
            ),
        dict(
                data = [
                    dict(
                                y = getgraphinfo()['y'],
                                x = [s for s in range(0,len(getgraphinfo()['y']))],
                                type='scatter'
                        )
                ],
                layout=dict(title='Humility')
            )
    ]
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("graph.html",
        title = 'TempGraph',
        username = User.query.get('id'),
        ids=ids,
        graphJSON = graphJSON)