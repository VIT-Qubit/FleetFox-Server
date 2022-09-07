from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Worker)
admin.site.register(WorkerLocationDetails)
admin.site.register(CustomerTicket)
admin.site.register(WorkerLiveLocation)