
from django.urls import path
from .views import *
from .admin_views import *
from .customer_views import *

urlpatterns = [
    path('worker-login',WorkerLogin.as_view()),
    path('authenticate-worker',AuthenticateWorker.as_view()),
    path('get-worker-data',WorkerDetails.as_view()),
    path('get-today-works',GetTodayWorks.as_view()),
    path('get-all-works',GetAllWorks.as_view()),
    path('complete-task',CompleteTask.as_view()),
    path('update-worker-location-live',UpdateLocationWorker.as_view()),
    path('update-ticket',UpdateTicket.as_view()),
    path('update-status',UpdateStatus.as_view()),

    #admin-urls
    path('get-worker-live-location',GetWorkerLocationDetails.as_view()),
    path('assign-worker',AssignWorker.as_view()),
    path('get-worker-distance-data',GetWorkerLocationData.as_view()),

    #customer-urls
    path('customer-register',Register.as_view()),
    path('create-ticket',CreateTicket.as_view())

]
