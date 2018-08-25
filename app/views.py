#! -*- coding: utf8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask_sqlalchemy import get_debug_queries
from werkzeug.urls import url_parse
from app import app, db, login, bp

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button1 = 3
button2 = 4

#initialize GPIO status variables
button1Sts = GPIO.LOW
button2Sts = GPIO.LOW

# Set button and PIR sensor pins as an input
GPIO.setup(button1, GPIO.IN)   
GPIO.setup(button2, GPIO.IN)

from datetime import datetime

import plotly
import pandas as pd
import numpy as np
import json

from app.emails import follower_notification, send_password_reset_email

from app.models import User, ROLE_USER, ROLE_ADMIN, Sensorsdb, Raspb3BPins, Post, Sensors
from app.models import Temp, NODATA

from app.forms import LoginForm, RegistrationForm, EditForm, AddSensor, PostForm, SearchForm, ResetPasswordRequestForm, ResetPasswordForm

from app.getfunc import getinfo, getgraphinfo, getlastinfo, update_temphum

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
        g.search_form = SearchForm()

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app.config['DATABASE_QUERY_TIMEOUT']:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', form=form)

@app.route('/search', methods = ['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, app.config['MAX_SEARCH_RESULTS']).all()
    return render_template('index/search_results.html',
        query = query,
        results = results)

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
    return render_template('auth/login.html', title='Sign In', form=form)

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
        user = User(username=username, email=form.email.data, role = ROLE_USER)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember = remember_me)
        #return redirect(url_for('index'))
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('auth/register.html', title='Register', form=form)

@app.route('/buttons', methods = ['GET', 'POST'])
@login_required
def buttons():
    # Read Sensors Status
    button1Sts = GPIO.input(button1)
    button2Sts = GPIO.input(button2)

    templateData = {
      'title' : 'GPIO input Status!',
      'button1'  : button1Sts,
      'button2'  : button2Sts
      }
    return render_template('rasp/buttons.html', result = getlastinfo(), **templateData)

@app.route("/buttons/<deviceName>/<action>")
@login_required
def buttons_action(deviceName, action):
    if deviceName == 'button1':
        actuator = button1
    if deviceName == 'button2':
        actuator = button2
   
    if action == "on":
        GPIO.setup(actuator, GPIO.OUT)   #устанавливаем пин на выходной сигнал
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.setup(actuator, GPIO.OUT)   #устанавливаем пин на выходной сигнал
        GPIO.output(actuator, GPIO.LOW)
             
    #button1Sts = GPIO.input(button1)
    #button2Sts = GPIO.input(button2)
   
    #templateData = {
    #            'title' : 'GPIO input Status info',
    #          'button1'  : button1Sts,
    #          'button2'  : button2Sts,
    #}
    return redirect(url_for('buttons')) #, result = getlastinfo(), **templateData))
    #return render_template('rasp/buttons.html', result = getlastinfo(), **templateData)

@app.route("/buttons/<tempdat>")
@login_required
def buttons_tempdat(tempdat):
    # Read Sensors Status
    #button1Sts = GPIO.input(button1)
    #button2Sts = GPIO.input(button2)
    update_temphum()

    #templateData = {
    #  'title' : 'GPIO input temp updated!',
    #  'button1'  : button1Sts,
    #  'button2'  : button2Sts
    #  }
    return redirect(url_for('buttons')) #, result = getlastinfo(), **templateData))
    #return render_template('rasp/buttons.html', result = getlastinfo(), **templateData)

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
    return render_template('index/edit.html',
        form = form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('usersettings', username = username))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + username + '.')
        return redirect(url_for('usersettings', username = username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + username + '!')
    follower_notification(user, g.user)
    return redirect(url_for('usersettings', username = username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('usersettings', username = username))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + username + '.')
        return redirect(url_for('usersettings', username = username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + username + '.')
    return redirect(url_for('usersettings', username = username))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post == None:
        flash('Post not found.')
        return redirect(url_for('index'))
    if post.author.id != g.user.id:
        flash('You cannot delete this post.')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('index'))

@app.errorhandler(401)
def page_not_found(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = g.user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    return render_template('index/index.html',
        title = 'Home',
        form = form,
        posts = posts)

@app.route('/rasp')
def rasp():
    pins = Raspb3BPins.query
    sens = Sensors.query
    return render_template('rasp/rsettings.html', title='Raspberry Pi config page', pins = pins, sens = sens)#, sens = sens)

@app.route('/pin_connect/<pin_id>')
def pin_connect(pin_id):
    sens = Sensorsdb.query
    return render_template('rasp/rconnect.html', title='Raspberry Pi connect page', pin_id = pin_id, sens=sens)

@app.route('/pin_connect_with_sensor/<pinid>/<sensid>')
def pin_connect_with_sensor(pinid, sensid):
    connect = Sensors(name = Sensorsdb.query.filter_by(id = sensid).first().name, raspin_id = pinid)
    db.session.add(connect)
    db.session.commit()
    return redirect(url_for('rasp'))

@app.route('/pin_delconnect/<sensid>')
def pin_delconnect(sensid):
    delconnect = Sensors.query.filter_by(id=sensid).first()
    db.session.delete(delconnect)
    db.session.commit()
    return redirect(url_for('rasp'))

@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def usersettings(username, page = 1):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('usersettings', username=g.user.username))
    posts = user.posts.paginate(page, app.config['POSTS_PER_PAGE_USER'], False)
    return render_template('index/usersettings.html',
        username = user,
        posts = posts,
        title='Settings page')

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('index/user_popup.html', user=user)


@app.route('/temp')
@app.route('/temp/<int:page>', methods = ['GET', 'POST'])
@login_required
def temp(page = 1):
    #result = Temp.all_my_temphum().paginate(page, app.config['POSTS_PER_PAGE'], False)
    result = Temp.query.order_by('-id').paginate(page, app.config['POSTS_PER_PAGE'], False)
    pages = len(Temp.query.order_by('-id').all()) // app.config['POSTS_PER_PAGE'] + bool(len(Temp.query.order_by('-id').all()) % app.config['POSTS_PER_PAGE'])
    #Temp.all_my_temphum().paginate(page, app.config['POSTS_PER_PAGE'], False)
    return render_template("rasp/temp.html",
        title = 'Home',
        username = User.query.get('id'),
        result = result,
        pages = pages,
        nowpage = page)


@app.route('/deltemp/<timeid>')
@login_required
def delete_from_temp(timeid):
    tempquery = Temp.query.filter_by(id=timeid).first()
    db.session.delete(tempquery)
    db.session.commit()
    return redirect(url_for('temp'))

@app.route('/swiki')
@login_required
def swiki():
    sensors = Sensorsdb.query
    return render_template("rasp/sensorsdb.html",
        title = 'Sensors database',
        username = User.query.get('id'),
        sensorsids = sensors
        )

@app.route('/addsensor', methods = ['GET', 'POST'])
@login_required
def addsensor():
    form = AddSensor()
    if form.validate_on_submit():
        sensor = Sensorsdb(name=form.name.data,about=form.about.data, pic=form.pic.data)
        db.session.add(sensor)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('swiki'))
    else:
        form.name.data = ""
        form.about.data = ""
        form.pic.data = ""
    return render_template('rasp/addsensor.html',
        title = "Add Sensor",
        formname = "addsensor",
        form = form)

@app.route('/editsensor/<pid>', methods = ['GET', 'POST'])
@login_required
def editsensor(pid):
    form = AddSensor()
    sensorquery = Sensorsdb.query.filter_by(id=pid).first()
    if form.validate_on_submit():
        editedsensor = sensorquery
        editedsensor.about = form.about.data
        editedsensor.name = form.name.data
        editedsensor.pic = form.pic.data
        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('swiki'))
    else:
        form.name.data = sensorquery.name
        form.about.data = sensorquery.about
        form.pic.data = sensorquery.pic
    return render_template('rasp/addsensor.html',
        title = "Edit Sensor",
        formname = "editsensor",
        form = form)

@app.route('/remove/<pid>', methods = ['GET', 'POST'])
@login_required
def removesensor(pid):
    sensorquery = Sensorsdb.query.filter_by(id=pid).first()
    db.session.delete(sensorquery)
    db.session.commit()
    return redirect(url_for('swiki'))

@app.route('/tempgrapth')
@login_required
def tempgrapth():
    graphs = [
        dict(
            data = [
                    
                dict(
                    y = getgraphinfo()['humi'],
                    x = getgraphinfo()['time'],
                    type='scatter',
                    name='Humility'
                    ),

                dict(
                    y = getgraphinfo()['temp'],
                    x = getgraphinfo()['time'],
                    type='scatter',
                    name='Temperature',
                    )
                ],
            layout=dict(title='Scaner info')
        )
    ]
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("rasp/graph.html",
        title = 'TempGraph',
        username = User.query.get('id'),
        ids=ids,
        graphJSON = graphJSON)