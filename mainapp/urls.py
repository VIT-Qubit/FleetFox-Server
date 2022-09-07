
from django.urls import path
from .views import *
from .admin_views import *

urlpatterns = [
    path('worker-login',WorkerLogin.as_view()),
    path('authenticate-worker',AuthenticateWorker.as_view()),
    path('get-worker-data',WorkerDetails.as_view()),
    path('get-today-works',GetTodayWorks.as_view()),
    path('complete-task',CompleteTask.as_view()),
    path('update-worker-location-live',UpdateLocationWorker.as_view()),
    path('sample-sms',SampleSms.as_view()),

    #admin-urls
    path('get-worker-live-location',GetWorkerLocationDetails.as_view()),
    path('assign-worker',AssignWorker.as_view()),
    path('get-worker-distance-data',GetWorkerLocationData.as_view())
]
