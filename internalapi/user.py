from easypydb import DB
import os
import time

from internalapi.response import *
from internalapi.cache import *
from internalapi.methods import *
from internalapi.borks import *

db = DB('db', os.getenv('dbToken'))
#print('users', db.data['users'].keys())

class user:
	class UserObject:
		def __init__(self, data):
			for i in data:
				exec(f'self.{i} = data[i]')
			self.json = data

		def isadmin(self):
			return Response(100, self.userid in ["0297414827289718", "9580755075745798"])

		def delete(self):
			backup = db['users'][str(self.userid)]
			db['backup'].append(backup)
			cache.remove('username', backup['username'])
			cache.remove('email', backup['email'])
			del db['users'][str(self.userid)]
			db.save()
			return Response(100)

		def isfollowing(self, memberId):
			print(memberId, self.following)
			return Response(100, memberId in self.following)

		def edit(self, attr, value):
			db['users'][self.userid].update({attr: value})
			db.save()
			return Response(100)
		
		def change_password(self, newPassword):
			newPassword = methods.passwordHash(newPassword).content
			self.edit("password", newPassword)
			return Response(100)

		def likebork(self, borkId):
			borkObj = borks.fetch(borkId)
			if borkObj.success:
				if borkId in db['users'][self.userid]['likedBorks']:
					return Response(200, "You have already liked this bork.")
				else:
					db['users'][self.userid]['likedBorks'].append(borkId)
					db.save()
					return Response(100)
			else:
				return Response(202, "Bork not found")
		
		def unlikebork(self, borkId):
			borkObj = borks.fetch(borkId)
			if borkObj.success:
				try:
					if borkId in db['users'][self.userid]['likedBorks']:
						db['users'][self.userid]['likedBorks'].remove(borkId)
						db.save()
						return Response(100)
					else:
						return Response(200, "You have not liked this bork.")
				except:
					return Response(202, "This account has not liked this bork")
			else:
				return Response(202, "Bork not found")
		
		def follow(self, tofollow):
			if self.isfollowing(tofollow).content:
				return Response(200, "Already following this user")
			else:
				db['users'][self.userid]['following'].append(tofollow)
				db['users'][tofollow]['followers'].append(self.userid)
				db.save()
				return Response(100)
		
		def unfollow(self, tounfollow):
			if self.isfollowing(tounfollow).content:
				db['users'][self.userid]['following'].remove(tounfollow)
				db['users'][tounfollow]['followers'].remove(self.userid)
				db.save()
				return Response(100)
			else:
				return Response(200, "Not following this user")

	def fetchAll():
		data = []
		for i in db['users'].keys():
			data.append(user.fetch(i).content)
		return Response(100, data)

	def create(data):
		if list(data.keys()) == ["username", "email", "password"]:
			if cache.get('username', data['username']).success:
				return Response(200, "Username already in use")
			elif cache.get('email', data['email']).success:
				return Response(200, "Email already in use")
			else:
				userId = methods.generateId(16).content
				passwordHash = methods.passwordHash(data["password"]).content
				timeCreated = int(time.time())
				db['users'].update({userId: {"userid": userId, "username": data["username"], "password": passwordHash, "created": timeCreated, "email_verified":False,"email": data['email'], "borks": [], "following": [], "followers": [], "bio": ""}})
				cache.set('username', data['username'], userId)
				cache.set('email', data['email'], userId)
				db.save()
				return Response(100, userId)
		else:
			return Response(201)
	
	def fetch(id):
		if len(id) == 16:
			if id in db['users']:
				return Response(100, user.UserObject(db['users'][id]))
			else:
				return Response(202, "Userid not Found")
		else:
			u = cache.get('username', id)
			if u.success:
				return Response(100, user.UserObject(db['users'][u.content]))
			else:
				return Response(202, "Username not Found")