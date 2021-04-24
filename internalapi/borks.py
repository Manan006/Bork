from easypydb import DB
import time
import internalapi

from internalapi.methods import *
from internalapi.response import *
from internalapi.user import *

db = DB('borkDB', '-BWrVIhyE_Xz-z3RmT3ib0p9WiK8RzuH6Yc2hXB0zJpovBqTKQ89HuamakfmlKD29ub6mkP2fhsViITWuYcSpg==')

class borks:
	class BorkObject:
		def __init__(self, borkId):
			data = db[borkId]
			self.borkId = borkId
			self.sender = internalapi.user.user.fetch(data["sender"])
			self.content = data["content"]
			self.likes = data["likes"]
			self.sent = data["sent"]
			self.root = data["root"]
			self.json = data

	def create(sender, content, root):
		borkId = methods.generateId(16).content
		db[borkId] = {"id": borkId, "sender": sender, "content": content, "root": root, "sent": int(time.time()), "likes": 0}
		user_obj = internalapi.user.user.fetch(sender).content
		borks = user_obj.borks
		borks.append(borkId)
		user_obj.edit("borks", borks)
		return Response(100, borkId)

	def fetch(borkId):
		if borkId in db.data:
			return Response(100, borks.BorkObject(borkId))
		else:
			return Response(202)
	
	def delete(borkId):
		bork = db[borkId]
		db['backup'].append(bork)
		del db[borkId]
		return Response(100)
	
	def edit(borkId, attr, value):
		db[borkId][attr] = value
		return Response(100)