from rest_framework.serializers import Serializer,ModelSerializer
from .models import *


class WorkerSerializer(ModelSerializer):
	class Meta:
		model=Worker
		fields='__all__'


class CustomerTicketSerializer(ModelSerializer):
	class Meta:
		model=CustomerTicket
		fields='__all__'

	def __init__(self,*args,**kwargs):
		super(CustomerTicketSerializer,self).__init__(*args,**kwargs)
		request=self.context.get("request")

		if request and request.method=="POST":
			self.Meta.depth=0
		elif request and request.method =="PUT":
			self.Meta.depth=0
		else:
			self.Meta.depth=4

class WorkerLocationDetailsSerializer(ModelSerializer):
	class Meta:
		model=WorkerLocationDetails
		fields='__all__'

class WorkerLiveLocatinSerializer(ModelSerializer):
	class Meta:
		model=WorkerLiveLocation
		fields=['data']