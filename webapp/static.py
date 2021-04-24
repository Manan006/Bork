from webapp.init import app

from internalapi.session import *

import flask

@app.route('/signup')
def signup():
	ss = session.fetch(flask.request)
	if ss.success:
		return flask.redirect('/')
	else:
		return flask.render_template('signup.html')

@app.route('/login')
def login():
	ss = session.fetch(flask.request)
	if ss.success:
		return flask.redirect('/')
	else:
		return flask.render_template('login.html')

@app.route('/')
def home():
	ss = session.fetch(flask.request)
	if ss.success:
		return flask.render_template('in/home.html')
	else:
		return flask.render_template('out/home.html')