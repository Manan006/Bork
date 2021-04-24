from webapp.init import app

import flask
import os
import json

from internalapi.cache import *
from internalapi.user import *
from internalapi.session import *

@app.route('/connect')
def connectwithtoken():
	t = flask.request.args.get('t')
	if t == None:
		return "Invalid connection token"
	else:
		c = cache.get('redirecttoken', t)
		if c.success:
			account = cache.get('redirecttoken', t).content
			response = flask.make_response(flask.redirect('https://' + os.getenv('domain')))
			sessionId = session.create(account).content
			cache.remove('redirecttoken', t)
			response.set_cookie('session', sessionId)
			return response
		else:
			return "Invalid connection token"

@app.route('/logout')
def logout():
	ss = session.fetch(flask.request)
	if ss.success:
		session.end(ss.id)
		response = flask.make_response(flask.render_template('in/logout.html'))
		response.set_cookie('session', '', expires=0)
		return response
	else:
		return flask.render_template('out/logout.html')