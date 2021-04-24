import random
import hashlib
import time
import os

from internalapi.response import Response
from internalapi.cache import *

class methods:
	def generateId(n):
		return Response(100, ''.join(random.choice('0123456789') for _ in range(n)))
	
	def generateToken(n):
	  return Response(100, ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(n)))

	def passwordHash(p):
		salt = methods.generateId(32).content
		password = salt + hashlib.sha512(bytes(salt + p, encoding="utf-8")).hexdigest()
		return Response(100, password)

	def verifyHash(p, hash):
		salt = hash[:32]
		check = salt + hashlib.sha512(bytes(salt + p, encoding="utf-8")).hexdigest()
		return Response(100, check == hash)
		
	def generateSessionId(n):
		while True:
			sessionId= ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(n))
			if not cache.get('session',sessionId).success:
				return Response(100, sessionId)
	
	def htmlescape(text):
		table = {
			"&": "&amp;",
			'"': "&quot;",
			"'": "&apos;",
			">": "&gt;",
			"<": "&lt;"
		}
		for x in table:
			text = text.replace(x, table[x])
		return Response(100, text)