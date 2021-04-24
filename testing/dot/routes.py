from webapp.init import app

from flask import render_template
import flask
from easypydb import DB
import os
import hashlib
from internalapi.verify import *
from internalapi.cache import cache
from internalapi.methods import methods
from internalapi.session import session
import internalapi
from internalapi.verify import verify
from internalapi.borks import borks

db = DB('db', os.getenv('dbToken'))

def gethex(n):
	return ''.join(random.choice('0123456789abcdef') for _ in range(n))

@app.route('/home')
def dotroute_home():
	sessionId = flask.request.cookies.get('session')
	if sessionId != None and cache.get('session', sessionId).success:
		user = user.fetch(cache.get('session', sessionId).content).content
		return render_template('home.html', username=user.username)
	else:
		return render_template('login.html')

@app.route('/dot')
def dot():
	return render_template("home.html",username="Dot")