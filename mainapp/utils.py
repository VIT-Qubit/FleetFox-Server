import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import datetime,pytz
from .models import *
from twilio.rest import Client
import random

def generate_token(data):
	return jwt.encode(data,settings.SECRET_KEY,algorithm="HS256")

def get_request_header(request):
	header=request.META.get('HTTP_AUTHORIZATION','')
	#print(header)
	return header


class WorkerAuthentication(BaseAuthentication):
	keyword="Bearer"
	def authenticate(self,request):

		auth=get_request_header(request).split()
		#print(auth)
		if not auth or auth[0].lower()!=self.keyword.lower():
			raise exceptions.AuthenticationFailed(_('Not authorised! Token is not provided'))

		#print("1")
		if(len(auth)==1):
			msg = _('Invalid token header. No credentials provided.')
			raise exceptions.AuthenticationFailed(msg)
		elif len(auth) > 2:
			msg = _('Invalid token header. Token string should not contain spaces.')
			raise exceptions.AuthenticationFailed(msg)

		token_=auth[1]

		try:
			decode_token=jwt.decode(token_,settings.SECRET_KEY,algorithms=['HS256'])

			if "id" not in decode_token.keys():
				raise exceptions.AuthenticationFailed(_('Invalid token.'))
			id=decode_token["id"]

			user=Worker.objects.filter(id=id)
			if user.exists():
				return (user[0],None)
			else:
				raise exceptions.AuthenticationFailed(_('Invalid token.'))
		except jwt.exceptions.InvalidSignatureError:
			raise exceptions.AuthenticationFailed(_('Invalid token given'))

		except jwt.exceptions.DecodeError:
			raise exceptions.AuthenticationFailed(_('Invalid token given'))

def get_current_date():
	return datetime.datetime.now(pytz.timezone("Asia/Kolkata")).date()

def convert_date(date):
	return datetime.date(year=int(date[0]),month=int(date[1]),day=int(date[2]))

def send_sms(number,code):
	client=Client(settings.TWILLIO_SID,settings.TWILLIO_AUTH)

	message=client.messages.create(
		from_='+14014094605',
		body=f'code-{code}',
		to=f'+91{number}')

	return message.sid

def generate_code():
	string_=[str(random.randint(0,9)) for _ in range(5)]
	return "".join(string_)


