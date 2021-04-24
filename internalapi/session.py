from internalapi.cache import *
from internalapi.methods import *
from internalapi.response import *
from internalapi.user import *

class session:
	def create(userid):
		sessionId = methods.generateId(64).content
		cache.set('session', sessionId, userid)
		return Response(100, sessionId)

	def get(sessionId):
		session = cache.get('session', str(sessionId))
		if session.success:
			return Response(100, user.fetch(session.content).content)
		else:
			return Response(202)
	
	def end(sessionId):
		session = cache.get('session', sessionId)
		if session.success:
			cache.remove('session', sessionId)
			return Response(100)
		else:
			return Response(202)
	
	class fetch:
		def __init__(self, flask_request):
			self.cookies = flask_request.cookies
			if "session" in self.cookies:
				ss = session.get(self.cookies["session"])
				if ss.success:
					self.success = True
					for i in ss.content.json:
						exec(f'self.{i} = ss.content.json["{i}"]')
					self.obj = user.fetch(self.userid).content
					self.id = self.cookies['session']
				else:
					self.success = False
			else:
				self.success = False