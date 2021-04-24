from webapp.init import app

from internalapi.cache import *
from internalapi.methods import *
from internalapi.user import *
from internalapi.session import *
from internalapi.verify import *

import string
import flask
import os
import regex as re

@app.route('/api/borks')
def api_borks():
	ss = session.fetch(flask.request)
	if ss.success:
		borks_to_return = []
		for followingId in ss.obj.following:
			followingObj = user.fetch(followingId)
			if followingObj.success:
				for borkId in followingObj.content.borks:
					borkObj = borks.fetch(borkId)
					if borkObj.success:
						borks_to_return.append(borkObj.content.json)
		borks_to_return = sorted(borks_to_return, key = lambda i: i["sent"], reverse=True)
		return {"Success": True, "borks": borks_to_return}
	else:
		return {"success": False, "error": "Invalid Session"}

@app.route('/api/borks/<userQuery>')
def api_borks_user(userQuery):
	ss = session.fetch(flask.request)
	if ss.success:
		user_lookup = user.fetch(userQuery)
		if user_lookup.success:
			borkstoreturn = []
			for borkId in user_lookup.content.borks:
				borkObj = borks.fetch(borkId)
				if borkObj.success:
					borkstoreturn.append(borkObj.content.json)
			return {"success": True, "borks": borkstoreturn}
		else:
			return {"success": False, "error": "Invalid user"}
	else:
		return {"success": False, "error": "Invalid session"}

@app.route('/api/sendbork', methods=['POST'])
def api_sendbork():
	ss = session.fetch(flask.request)
	if ss.success:
		form = flask.request.form
		if not "content" in form:
			return {"success": False, "error": "No content"}
		elif not "root" in form:
			return {"success": False, "error": "No root"}
		elif form['root'] != '.':
			return {"success": False, "error": "Invalid root"}
		else:
			createdBork = borks.create(ss.userid, form['content'], form['root'])
			if not createdBork.success:
				return {"success": False, "error": createdBork.content}
			else:
				return {"success": True, "bork": borks.fetch(createdBork.content).content.json}
	else:
		return {"success": False, "error": "Invalid session"}

@app.route('/api/deletebork', methods=['POST'])
def api_delete_bork():
	ss = session.fetch(flask.request)
	if ss.success:
		if flask.request.form['borkId'] in ss.borks:
			borkId = flask.request.form['borkId']
			bork_data = ss.borks
			bork_data.remove(borkId)
			ss.obj.edit('borks', bork_data)
			borks.delete(borkId)
			return {"success": True}
		else:
			return {"success": False, "error": "Invalid bork Id"}
	else:
		return {"success": False, "error": "Invalid session"}

@app.route('/api/getbork')
def api_getbork():
	ss = session.fetch(flask.request)
	if ss.success:
		borkId = flask.request.args.get('borkId')
		if borkId == None:
			return {"success": False, "error": "No borkId provided"}
		borkObj = borks.fetch(borkId)
		if borkObj.success:
			hasliked = False
			if borkId in ss.obj.likedBorks:
				hasliked = True
			returnData = borkObj.content.json
			returnData.update({"hasliked": hasliked})
			return borkObj.content.json
		else:
			return {"success": False, "error": "Bork does not exist"}, 404
	else:
		return {"success": False, "error": "Invalid session"}

@app.route('/api/like', methods=['POST'])
def api_likebork():
	ss = session.fetch(flask.request)
	if ss.success:
		borktolike = borks.fetch(flask.request.form["borkId"])
		if borktolike.success:
			borktolike = borktolike.content.borkId
			if not borktolike in ss.likedBorks:
				ss.obj.likebork(borktolike)
				return {"success": True}
			else:
				return {"success": False, "error": "You have already liked this bork"}
		else:
			return {"success": False, "error": "This bork does not exist"}
	else:
		return {"success": False, "error": "Invalid session"}

@app.route('/api/unlike', methods=['POST'])
def api_unlikebork():
	ss = session.fetch(flask.request)
	if ss.success:
		borktounlike = borks.fetch(flask.request.form["borkId"])
		if borktounlike.success:
			borktounlike = borktounlike.content.borkId
			if borktounlike in ss.likedBorks:
				ss.obj.unlikebork(borktounlike)
				return {"success": True}
			else:
				return {"success": False, "error": "You have already liked this bork"}
		else:
			return {"success": False, "error": "This bork does not exist"}
	else:
		return {"success": False, "error": "Invalid session"}
		
@app.route('/api/follow', methods=['POST'])
def api_follow():
	ss = session.fetch(flask.request)
	if ss.success:
		tofollow = user.fetch(flask.request.form["follow"]).content.userid
		if not tofollow in ss.following:
			ss.obj.follow(tofollow)
			return {"success": True}
		else:
			return {"success": False, "error": "You are already following this account"}
	else:
		return {"success": False, "error": "Invalid session"}

@app.route('/api/unfollow', methods=['POST'])
def api_unfollow():
	ss = session.fetch(flask.request)
	if ss.success:
		tofollow = user.fetch(flask.request.form["follow"]).content.userid
		if tofollow in ss.following:
			ss.obj.unfollow(tofollow)
			return {"success": True}
		else:
			return {"success": False, "error": "You are not following this account"}
	else:
		return {"success": False, "error": "Invalid session"}

@app.route('/api/changepassword', methods=['POST'])
def api_change_password():
	ss = session.fetch(flask.request)
	if not ss.success:
		return {"success": False, "message": "Invalid session"} 	
	form = flask.request.form
	if not methods.verifyHash(form['old_password'], ss.password).success:
		return {"success":False, "message": "The entered password is incorrect"}
	ss.obj.change_password(form['new_password'])
	return {"success": True, "message": "Password changed successfully!"}

@app.route('/api/changeemail', methods=['POST'])
def api_change_email():
	ss = session.fetch(flask.request)
	if not ss.success:
		return {"success": False, "message": "Invalid session"} 
	user = ss.obj
	form = flask.request.form
	new_email = form['email']
	user.edit("email", new_email)
	user.edit("email_verified", False)
	cache.set("email", new_email, user.userid)
	verify.email.sendVerifyEmail(user.userid)
	return {"success": True, "message": "Your email has been changed. We have sent a verification email to you."}

validUsernameRE = re.compile(r'^[A-z0-9._]{1,15}$')

@app.route('/api/createaccount', methods=['POST'])
def api_create_account():
	form = flask.request.form
	username = form['username']

	usernameValid = validUsernameRE.match(username)

	if len(username) == 0:
		return {"error": "Username too short"}

	if len(username) > 15:
		return {"error": "Username too long"}

	if not usernameValid:
		return {"error": "Username contains invalid characters"}

	create_user = user.create(
		{
			"username": username, 
			"email": form['email'], 
			"password": form['password']
		}
	)
	if create_user.success:
		redirecttoken = methods.generateToken(32).content
		cache.set('redirecttoken', redirecttoken, create_user.content)
		internalapi.verify.verify.email.sendVerifyEmail(create_user.content)
		return {"success": True, "logintoken": redirecttoken}
	else:
		return {"success": False, "error": create_user.content}

@app.route('/verify_email/<verification_code>')
def verifyEmail(verification_code):
	user_id = cache.get('verifyEmailLink',verification_code)
	if user_id.success and verification_code == cache.get('verifyEmail', user_id.content).content:
		user_id = user_id.content
		userObj = user.fetch(user_id).content
		userObj.edit('email_verified', True)
		cache.remove("verifyEmail", user_id)
		cache.remove('verifyEmailLink', verification_code)
		return "Verified!"
	else:
		return "Invalid or Used Verification link"

@app.route('/api/connect', methods=['POST'])
def api_connect(): 
	form = flask.request.form
	connectinguser = user.fetch(form['username'])
	if not connectinguser.success:
		return connectinguser.content
	connectinguser = connectinguser.content
	print('cuc', connectinguser.password, connectinguser.username, form['password'])
	validHash = methods.verifyHash(
		form['password'],
		connectinguser.password
	).content
	print('vh', validHash)
	if not validHash:
		return {"success": False, "message": "Invalid password or username"}
	token = methods.generateToken(32).content
	cache.set('redirecttoken', token, connectinguser.userid)
	return {"success": True, "redirecttoken": token}