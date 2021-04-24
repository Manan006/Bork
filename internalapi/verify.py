from internalapi.cache import *
from internalapi.methods import *
from internalapi.user import *
import smtplib

defaultMessage="Please Click on the link to verify email "
import os
class verify:
	def create_random(n):
	  return Response(100, ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(n)))
		
	class email:
		def sendVerifyEmail(userId,message=defaultMessage):
			#reciever is needed all the time,
			#message is optional, and can be used as the default one incase if it's not provided
			sender= smtplib.SMTP('smtp.gmail.com', 587)
			sender.starttls()
			sender.login(os.getenv('verfiyEmail'),os.getenv('verifyEmailPass'))
			link=verify.email.create_link(userId)
			reciever=user.fetch(userId).content.email
			message=message+os.getenv("domain")+"/verify_email/"+link
			sender.sendmail(os.getenv('verfiyEmail'), reciever, message)
			cache.set('verifyEmailLink',link,userId)
			cache.set('verifyEmail',userId,link)
			sender.quit()

		def create_link(user_id):
			while True:
				link=verify.create_random(32).content
				if cache.get("verfiyEmailLink",link).code==202:
					break
			#the above code is to generate a random code which is not being used right now
			
			return link