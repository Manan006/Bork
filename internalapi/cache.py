from easypydb import DB

SC = DB('cache', "B1Wt0HBuyF7stPFQ35WuqeB3IaV-cIsmIx8daTLU_JklJYRdixT8mAjXOkb6ZCEnTIeh8G3hLG41HT3T4YALSQ==")

from internalapi.response import Response

class cache:
	def set(namespace, key, data):
		key = key.lower()
		SC[namespace + '_' + key] = data
		return Response(100)

	def get(namespace, key):
		key = key.lower()
		if namespace + '_' + key in SC.data:
			return Response(100, SC[namespace + '_' + key])
		else:
			return Response(202)
	
	def remove(namespace, key):
		key = key.lower()
		if namespace + '_' + key in SC.data:
			del SC[namespace + '_' + key]
			return Response(100)
		else:
			return Response(202)