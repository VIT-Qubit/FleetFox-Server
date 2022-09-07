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


class WorkerLocationDetailsSerializer(ModelSerializer):
	class Meta:
		model=WorkerLocationDetails
		fields='__all__'

class WorkerLiveLocatinSerializer(ModelSerializer):
	class Meta:
		model=WorkerLiveLocation
		fields=['data']