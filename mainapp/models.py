from django.db import models

class Customer(models.Model):
	name =models.CharField(max_length=256,null=True,blank=True)
	age=models.IntegerField()
	gender=models.CharField(max_length=1,null=True,blank=True)
	address=models.TextField()
	pincode=models.CharField(max_length=10,null=True,blank=True)
	lat=models.CharField(max_length=256,null=True,blank=True)
	lon=models.CharField(max_length=256,null=True,blank=True)
	json=models.JSONField(null=True,blank=True)

class Admin(models.Model):
	email=models.CharField(max_length=256)
	name=models.CharField(max_length=256)
	age=models.IntegerField()
	password=models.CharField(max_length=256)
	pincodes=models.JSONField(null=True,blank=True)
	json=models.JSONField(null=True,blank=True)

class Worker(models.Model):
	name=models.CharField(max_length=256)
	age=models.IntegerField()
	worker_pincode=models.JSONField(null=True,blank=True)
	phone_number=models.CharField(max_length=10,null=True,blank=True)
	json=models.JSONField(null=True,blank=True)
	online=models.BooleanField(default=False)
	servicing=models.BooleanField(default=False)
	
class WorkerLiveLocation(models.Model):
	worker_id=models.ForeignKey(Worker,on_delete=models.CASCADE)
	data=models.JSONField(null=True,blank=True)
	date=models.DateField()




class WorkerLocationDetails(models.Model):
	worker_id=models.ForeignKey(Worker,on_delete=models.CASCADE,blank=True,null=True)
	data=models.JSONField(null=True,blank=True)
	json=models.JSONField(null=True,blank=True)
	date_of_service=models.DateField(null=True,blank=True)
	

class CustomerTicket(models.Model):
	customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
	admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE,null=True,blank=True)
	worker_assigned=models.BooleanField()
	ticket_type=models.CharField(max_length=500,null=True,blank=True)
	worker_id=models.ForeignKey(Worker,on_delete=models.CASCADE,null=True,blank=True)
	description=models.TextField(null=True,blank=True)
	completed=models.BooleanField(null=True,blank=True,default=False)
	reason=models.TextField(null=True,blank=True)
	datetime=models.DateTimeField(auto_now_add=True)
	service_date=models.DateField(null=True,blank=True)
	json=models.JSONField(null=True,blank=True)


