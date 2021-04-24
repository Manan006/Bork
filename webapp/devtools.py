from webapp.init import app

from internalapi.session import *
from internalapi.session import *
from internalapi.methods import *

import internalapi
import json
import os
import flask
import requests

def POST(url, payload, sessionId):
	return requests.post(url, data=payload, cookies={"session": sessionId}).text

def GET(url, sessionId):
	return requests.get(url, cookies={"session": sessionId}).text

@app.route('/whoami')
def whoami(): 
	sessionId = flask.request.cookies.get('session')
	sessiondata = session.get(str(sessionId))
	if sessiondata.success:
		return '<pre>' + json.dumps(user.fetch(sessiondata.content.userid).content.json, indent=4) + '</pre>'
	else:
		return "log in first"

@app.route('/console')
def devtools():
	return flask.render_template('console.html')

@app.route('/console/exec', methods=["POST"])
def devtool_exec():
	sessioncookie = flask.request.cookies.get('session')
	if sessioncookie == None: isadmin = False
	else: isadmin = user.fetch(session.get(sessioncookie).content.userid).content.isadmin().content
	if isadmin:
		code = flask.request.form['code']
		try:
			if code.startswith('POST '):
				code = code[5:]
				url = code.split(' ')[0]
				payload = eval(' '.join(code.split(' ')[1:]))
				return '<pre style="color: white;">' + POST('https://bork.shiba.life' + url, payload, sessioncookie) + '</pre>'
			elif code.startswith('GET '):
				code = code[4:]
				return '<pre style="color: white;">' + GET('https://bork.shiba.life' + code, sessioncookie) + '</pre>'
			else:
				resp = eval(code)
				if type(resp) == dict:
					return '<pre style="color: white;">' + json.dumps(resp, indent=4) + '</pre>'
				else:
					return '<pre style="color: white;">' + methods.htmlescape(str(resp)).content + '</pre>'
		except Exception as e:
			resp = "<error style='color: #f54747;'> Error: " + str(e) + "</error>"
		return resp
	else:
		return "<lmao style='color: #cc47f5'>you goddamn clown</lmao>"