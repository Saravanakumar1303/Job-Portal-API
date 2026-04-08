from django.urls import path
from .views import *

urlpatterns =[
    path('job_list/',JobListAPIView.as_view(), name="jobs-create-view"),
    path('job_list/<int:pk>/update/',JobUpdateAPIView.as_view(), name="job-update"),
    path('job_list/<int:pk>/delete/',JobDeleteAPIView.as_view(), name="job-delete"),
]