from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .utils import *

from .serializers import *
import datetime
# Create your views here.



class UpdateStatus(APIView):
	authentication_classes=[WorkerAuthentication]
	permission_classes=[]

	def post(sefl,request,format=None):

		worker=Worker.objects.get(id=request.user.id)
		data=request.data.get("type")
		if data=="online":
			worker.online=True
			worker.save()
		elif data=="offline":
			worker.online=False
			worker.save()

		return Response({
			"data":WorkerSerializer(worker).data
			},status=status.HTTP_200_OK)

class UpdateTicket(APIView):

	authentication_classes=[WorkerAuthentication]
	permission_classes=[]

	def post(self,request,format=None):
		data=request.data.get("type")
		ticket_id=request.data.get("ticket_id")

		if data=="START":
			customer_ticket=CustomerTicket.objects.get(id=ticket_id)
			customer_ticket.started=True
			customer_ticket.start_time=datetime.datetime.now().time()
			customer_ticket.save()

		elif data=="END":
			customer_ticket=CustomerTicket.objects.get(id=ticket_id)
			customer_ticket.ended=True
			customer_ticket.end_time=datetime.datetime.now().time()

		return Response({
			"Data":"Updated Successfully"
			},status=status.HTTP_200_OK)




class WorkerLogin(APIView):

	authentication_classes=[]
	permission_classes=[]

	def post(self,request,format=None):
		mobilenumber=request.data.get("mobilenumber")
		worker=Worker.objects.filter(phone_number=mobilenumber)
		if len(worker)==0:
			return Response({
				"Error":"worker Not Found"
				},status=status.HTTP_200_OK)
		else:
			worker=worker[0]

		workerotp=WorkerOtp.objects.filter(worker=worker)
		if len(workerotp)==0:
			workerotp=WorkerOtp.objects.create(worker=worker)
			workerotp.otp=generate_code()
			workerotp.code=generate_code()
			workerotp.validity=datetime.datetime.now()+datetime.timedelta(minutes=3)
			workerotp.save()
		else:
			workerotp=workerotp[0]
			validity_time=workerotp.validity
			if validity_time>timezone.now():
				pass
			else:
				workerotp.otp=generate_code()
				workerotp.code=generate_code()
				workerotp.validity=datetime.datetime.now()+datetime.timedelta(minutes=3)
				workerotp.save()

		send_sms(mobilenumber,workerotp.otp)

		#token=generate_token({"id":Worker.objects.get(id=1).id})

		return Response({
			"otp":workerotp.otp,
			"code":workerotp.code
			},status=status.HTTP_200_OK)



class AuthenticateWorker(APIView):

	def post(self,request,format=None):
		otp=request.data.get("otp")
		code=request.data.get("code")

		workerotp=WorkerOtp.objects.filter(otp=otp).filter(code=code)
		if len(workerotp)>0:
			workerotp=workerotp[0]
		else:
			print("here")
			return Response({
				"Error":"worker not found"
				},status=status.HTTP_400_BAD_REQUEST)

		if workerotp.validity>timezone.now():
			token=generate_token({"id":workerotp.worker.id})
			return Response({
				"token":token
				},status=status.HTTP_200_OK)
		else:
			return Response({
				"Error":"Invalid Otp given"
				},status=status.HTTP_400_BAD_REQUEST)

class WorkerDetails(APIView):

	authentication_classes=[WorkerAuthentication]
	permission_classes=[]

	def get(self,request,format=None):

		worker=WorkerSerializer(request.user)

		return Response({
			"Data":worker.data
			},status=status.HTTP_200_OK)

class GetTodayWorks(APIView):

	authentication_classes=[WorkerAuthentication]
	permission_classes=[]

	def get(self,request,format=None):

		count_data={}
		customer_tickets_for_today=CustomerTicket.objects.filter(worker_id=request.user).filter(completed=False).filter(service_date=get_current_date())
		count_data["total"]=len(CustomerTicket.objects.filter(worker_id=request.user).filter(service_date=get_current_date()))
		count_data["remaining"]=len(CustomerTicket.objects.filter(worker_id=request.user).filter(completed=False).filter(service_date=get_current_date()))
		count_data["completed"]=count_data["total"]-count_data["remaining"]
		customer_ticket_not_completed=CustomerTicket.objects.filter()

		customer_ticket_serializer=CustomerTicketSerializer(customer_tickets_for_today,many=True)

		return Response({
			"online":request.user.online,
			"Data":customer_ticket_serializer.data,
			"status_data":count_data
			},status=status.HTTP_200_OK)


class UpdateLocationWorker(APIView):

	authentication_classes=[WorkerAuthentication]
	permission_classes=[]

	def post(self,request,format=None):

		"""
			"lat":"current lat"
			"lon":"current lon"
		"""

		data=request.data.get("data")
		worker=Worker.objects.get(id=request.user.id)

		if worker.servicing==True:
			data["status"]="Servicing"
		else:
			data["status"]="Travelling"


		worker_live_location=WorkerLiveLocation.objects.filter(worker_id=request.user.id).filter(date=get_current_date())
		if len(worker_live_location)==0:
			worker_live_location=WorkerLiveLocation.objects.create(worker_id=request.user,data={"data":[]},date=get_current_date())

		else:
			worker_live_location=worker_live_location[0]


		worker_live_location_json=worker_live_location.data
		
		worker_live_location_json["data"].append(data)
		print(worker_live_location_json["data"])
		worker_live_location.data=worker_live_location_json
		worker_live_location.save()
		return Response({
			"msg":"ok"
			},status=status.HTTP_200_OK)

class CompleteTask(APIView):

	authentication_classes=[WorkerAuthentication]
	permission_classes=[]
	"""
		API to update if the work is completed...

	"""
	def post(self,request,format=None):

		"""

			"customer_id":{
				
				"customer_id":"stirng"
				"time_spent":number
			}

		"""

		data=request.data.get("data")
		current_date=get_current_date()
		worker_location_details=WorkerLocationDetails.objects.filter(worker_id=request.user).filter(date_of_service=current_date)

		if len(worker_location_details)==0:
			worker_location_details=WorkerLocationDetails.objects.create(worker_id=request.user,date_of_service=current_date,json={},data={})
		else:
			worker_location_details=worker_location_details[0]
		print(worker_location_details.json)
		worker_location_details_json=worker_location_details.json
		
		worker_location_details_json[str(data["customer_id"])]=data
		print(worker_location_details_json)
		worker_location_details.json=worker_location_details_json
		worker_location_details.save()

		worker_location_details_serializer=WorkerLocationDetailsSerializer(worker_location_details)
		return Response({
			"data":worker_location_details_serializer.data
			},status=status.HTTP_200_OK)
