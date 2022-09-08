from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .utils import *
from .serializers import *


class Register(APIView):

	def post(self,request,format=None):

		name=request.data.get("name")
		age=request.data.get("age")
		gender=request.data.get("gender")
		address=request.data.get("address")
		pincode=request.data.get("pincode")
		lat=request.data.get("lat")
		lon=request.data.get("lon")

		customer=Customer.objects.create(name=name,age=age,gender=gender,address=address,pincode=pincode,lat=lat,lon=lon)

		return Response({
			"Msg":"Customer created Successfully"
			},status=status.HTTP_200_OK)

class CreateTicket(APIView):

	def post(self,request,format=None):
		customer=Customer.objects.get(id=1)

		ticket_type=request.data.get("type")
		description=request.data.get("description")
		reasong=request.data.get("reason","")

		Customer_ticket=CustomerTicket.objects.create(customer_id=customer,ticket_type=ticket_type,description=description,reason=reason)
		return Response({
			"Msg":"Your ticket has been created Successfully"
			},status=status.HTTP_200_OK)


