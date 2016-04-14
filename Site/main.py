#!/usr/bin/env python

import dataset
import simplejson as json
import time
import re
from functools import wraps
from base64 import b64decode
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask.ext.seasurf import SeaSurf

app = Flask(__name__)
csrf = SeaSurf(app)

db = None
config = None

def login_required(f):
    """Ensures that an user is logged in"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect("/error/login_required")
        return f(*args, **kwargs)
    return decorated_function

def get_user():
    """Looks up the current user in the database"""

    login = 'user_id' in session    
    if login:
        return (True, db['users'].find_one(id=session['user_id']))

    return (False, None)

@app.errorhandler(404)
def page_not_found(e):
	return redirect('/error/page_not_found')

@app.errorhandler(500)
def i_broke_it(e):
	return redirect('/error/server_error')

@app.route('/error/<msg>')
def error(msg):
    """Displays an error message"""

    message = msg

    login, user = get_user()

    render = render_template('frame.html', page='error.html', 
        message=message, login=login, user=user)
    return make_response(render)

@app.route('/license')
def license():
	"""Displays license page"""
	
	login, user = get_user()
	
	render = render_template('frame.html', page='license.html',
		login=login, user=user)
	return make_response(render)

@app.route('/terms')
def terms():
    """Displays terms page"""

    login, user = get_user()

    render = render_template('frame.html', page='terms.html',
        login=login, user=user)
    return make_response(render)

@app.route('/privacy')
def privacy():
    """Displays privacy page"""

    login, user = get_user()

    render = render_template('frame.html', page='privacy.html',
        login=login, user=user)
    return make_response(render)

def session_login(username):
    """Initializes the session with the current user's id"""
    user = db['users'].find_one(username=username)
    session['user_id'] = user['id']

@app.route('/login', methods = ['POST'])
def login():
    """Attempts to log the user in"""

    from werkzeug.security import check_password_hash

    username = request.form['user']
    password = request.form['password']
	
    username = username.lower()
    username = username[:1].upper() + username[1:]

    user = db['users'].find_one(username=username)
    if user is None:
        return redirect('/error/invalid_credentials')

    if check_password_hash(user['password'], password):
        session_login(username)
        return redirect('/')

    return redirect('/error/invalid_credentials')

@app.route('/register')
def register():
    """Displays the register form"""

    # Render template
    render = render_template('frame.html', page='register.html', login=False, minpasslength=minpasslength)
    return make_response(render)
	
@app.route('/register/submit', methods = ['POST'])
def register_submit():
    """Attempts to register a new user"""

    from werkzeug.security import generate_password_hash

    username = request.form['user']
    password = request.form['password']

    username = username.lower()
    username = username[:1].upper() + username[1:]

    if not username:
        return redirect('/error/empty_user')

    user_found = db['users'].find_one(username=username)
    if user_found:
        return redirect('/error/already_registered')
    
    if len(password) < minpasslength:
        return redirect('error/password_too_short')
	
    new_user = dict(hidden=0, username=username, 
        password=generate_password_hash(password), roID=0, confirmed=False)

    # Set up the user id for this session
    session_login(username)

    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    """Logs the current user out"""

    del session['user_id']
    return redirect('/')

@app.route('/')
def index():
    login, user = get_user()
	# Render template
    render = render_template('frame.html',
        page='main.html', login=login, user=user, testing=config["testing"])
    return make_response(render)

if __name__ == '__main__':
    config_str = open('config.json', 'rb').read()
    config = json.loads(config_str)

    minpasslength = config['minimum_password_length']
    app.secret_key = config['secret_key']

    db = dataset.connect(config['db'])
	
    app.run(host=config["host"],port=config["port"],debug=config["debug"],threaded = True)
