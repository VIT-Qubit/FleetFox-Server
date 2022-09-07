from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .utils import *
from .serializers import *


class GetWorkerLocationDetails(APIView):

	def get(request,self,format=None):

		worker_live_location=WorkerLiveLocation.objects.filter(date=get_current_date())
		for i in worker_live_location:
			i.data["data"]=[i.data["data"][-1]]
		
		print(worker_live_location[0].data)

		worker_live_location_serializer=WorkerLiveLocatinSerializer(worker_live_location,many=True)
		print(worker_live_location_serializer.data)
		return Response({
			"data":worker_live_location_serializer.data
			},status=status.HTTP_200_OK)

class AssignWorker(APIView):

	def post(self,request,format=None):

		ticket_id=request.data.get("customer_ticket_id")
		Customer_ticket=CustomerTicket.objects.filter(id=ticket_id)
		if len(Customer_ticket)==0:
			return Response({
				"Err":"Ticket not found"
				})

		else:
			Customer_ticket=Customer_ticket[0]

		customer_pincode=Customer_ticket.customer_id.pincode

		workers=Worker.objects.all()
		min_count=999
		min_worker=None
		
		for i in workers:
			if customer_pincode in i.worker_pincode["data"]:
				count_=len(CustomerTicket.objects.filter(worker_id=i).filter(completed=False).filter(service_date=get_current_date()))
				if count_<min_count:
					min_count=count_
					min_worker=i

		Customer_ticket.worker_assigned=True
		Customer_ticket.worker_id=min_worker
		Customer_ticket.save()
		return Response({
			"Msg":"Worker Assigned"
			},status=status.HTTP_200_OK)






class GetWorkerLocationData(APIView):


	def get(self,request,format=None):

		worker_id=request.query_params.get("worker_id")
		worker=Worker.objects.get(id=worker_id)
		date=request.query_params.get("date")
		date_split=date.split(":")
		if len(date_split)<3:
			return Response({
				"Error":"Date error"
				},status=HTTP_400_BAD_REQUEST)


		date_converted=convert_date(date_split)
		print(date_converted)
		worker_location_details=WorkerLocationDetails.objects.filter(date_of_service=date_converted).filter(worker_id=worker)
		worker_location_serializer=WorkerLocationDetailsSerializer(worker_location_details,many=True)

		return Response({
			"data":worker_location_serializer.data
			},status=status.HTTP_200_OK)

class SampleSms(APIView):

	def get(self,request,format=None):

		s=send_sms()
		return Response({
			"data":s
			},status=status.HTTP_200_OK)

