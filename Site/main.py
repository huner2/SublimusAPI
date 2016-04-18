#!/usr/bin/env python

import dataset
import simplejson as json
import time
import re
import urllib2
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
	
@app.route('/about')
def about():
	"""Displays about page"""
	
	login, user = get_user()
	
	render = render_template('frame.html', page='about.html',
		login=login, user=user)
	return make_response(render)

@app.route('/apis')
def apis():
	"""Displays api page"""
	
	login, user = get_user()
	
	render = render_template('frame.html', page='apis.html',
		login=login, user=user)
	return make_response(render)

@app.route('/apis/getUsernameById/<uid>', methods=['GET'])
def getUsernameById(uid):
	"""Get user by ID"""
	try:
		userpage = urllib2.urlopen("http://www.roblox.com/users/" + uid + "/profile")
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})
	
	page_source = userpage.read()

	index = page_source.find("<h2>", page_source.find("header-title"))
	endIndex = page_source.find("</h2>", index)
	username = page_source[index+4:endIndex] # Add tag length
	return jsonify({'response': 200, 'username': username})

@app.route('/apis/userCanManageAsset/<uid>/<aid>', methods=['GET'])
def userCanManageAsset(uid, aid):
	"""Return if a user can manage an asset"""
	
	try:
		apicall = urllib2.urlopen("http://api.roblox.com/users/"+uid+"/canmanage/"+aid)
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})

	page_source = apicall.read()
	jsony = json.loads(page_source)
	
	if jsony["Success"] == False:
		return jsonify({'response': -1337})
	
	return jsonify({'response': 200, 'manage': jsony["CanManage"]})
	
@app.route('/apis/userHasAsset/<uid>/<aid>', methods=['GET'])
def userHasAsset(uid, aid):
	"""Return if a user has an asset"""
	try:
		apicall = urllib2.urlopen("http://api.roblox.com/ownership/hasasset?userId="+uid+"&assetId="+aid)
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})

	page_source = apicall.read()
	
	return jsonify({'response': 200, 'has':page_source})
	
@app.route('/apis/getMarketplaceInfo/<aid>', methods=['GET'])
def getMarketPlaceInfo(aid):
	"""Return product info for given product"""
	
	try:
		apicall = urllib2.urlopen("http://api.roblox.com/marketplace/productinfo?assetId="+aid)
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})
		
	page_source = apicall.read()
	
	return jsonify({'response': 200, 'info':page_source})
	
@app.route('/apis/getClanByUser/<uid>', methods=['GET'])
def getClanByUser(uid):
	"""Get clan information for given user id"""
	
	try:
		apicall = urllib2.urlopen("http://api.roblox.com/clans/get-by-user?userId="+uid)
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})
	
	page_source = apicall.read()
	
	return jsonify({'response': 200, 'info':page_source})
	
@app.route('/apis/getClanById/<cid>', methods=['GET'])
def getClanById(cid):
	"""Get clan information for given clan id"""
	
	try:
		apicall = urllib2.urlopen("http://api.roblox.com/clans/get-by-id?clanId="+cid)
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})
		
	page_source = apicall.read()
	
	return jsonify({'response': 200, 'info':page_source})
"""
@app.route('/apis/getFriendsOfUser/<uid>/<page>', methods=['GET'])
def friendsOfUser(uid, page):
	"""Get a paged list of friends for the  specified user"""

	try:
		apicall = urllib2.urlopen("http://api.roblox.com/users/"+uid+"/friends?page="+page)
	except urllib2.HTTPError, err:
		return jsonify({'reponse': err.code})

	page_source = apicall.read()

	return jsonify({'response': 200, 'info': page_source})

@app.route('/apis/getUserFriendshipCount/<uid>', methods=['GET'])
def getUserFriendshipCount(uid):
	"""Get the count of friends a user has"""

	try:
		apicall = urllib2.urlopen("http://api.roblox.com/user/get-friendship-count?userId="+uid)
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})

	page_source = apicall.read()

	jsony = json.loads(page_source)
	if jsony["success"] == False:
		return jsonify({'response': -1337})

	return jsonify({'response': 200, 'count': jsony["count"]})

@app.route('/apis/getUserFollowingExists/<uid>/<fid>',methods=['GET'])
def getUserFollowingExists(uid, fid):
	"""Return whether a user is following another, uid being the one following, the fid being the user being followed"""

	try:
		apicall = urllib2.urlopen("http://api.roblox.com/user/following-exists?userId="+fid+"&followerUserId="+uid)
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})

	page_source = apicall.read()

	jsony = json.loads(page_source)
	if jsony["success"] == False:
		return jsonify({'response': -1337})

	return jsonify({'response': 200, 'isFollowing': jsony['isFollowing']})

@app.route('/apis/getUserFollowers/<uid>/<page>'):
	"""Return the list of followers of a given user"""

	try:
		apicall = urllib2.open("http://api.roblox.com/users/followers?userId="+uid+"&page="+page)
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})

	page_source = apicall.read()

	return jsonify({'response': 200, 'followers': page_source})
"""
@app.route('/apis/getIdByUsername/<username>', methods=['GET'])
def getIdByUsername(username):
	"""Get ID by user"""
	
	try:
		search = urllib2.urlopen("http://m.roblox.com/User/DoSearch?startRow=0&keyword="+username)
	except urllib2.HTTPError, err:
		return jsonify({'response': err.code})

	page_source = search.read()
	
	index = page_source.find("alt=")
	endIndex = page_source.find("/>", index)
	firstUsername = page_source[index+5:endIndex-3]
	
	if (username.lower() != firstUsername.lower()):
		return jsonify({'response': -1337})
	
	index = page_source.find("/users")
	endIndex = page_source.find(">", index)
	id = page_source[index + 7:endIndex-1]
	
	return jsonify({'response': 200, 'id': id})

def session_login(username):
    """Initializes the session with the current user's id"""
    user = db['users'].find_one(username=username)
    session['user_id'] = user['id']


@app.route('/login')
def loginPage():
    """Displays the login page"""

    login, user = get_user()

    render = render_template('frame.html', page='login.html',
        login=login, user=user)

    return make_response(render)

@app.route('/logins', methods = ['POST'])
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
