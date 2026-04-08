from .views import *
from django.urls import path

urlpatterns =[
    path("jobapply/",JobApplyAPIView.as_view(), name="job-apply"),
    path("recruiterview/",RecruiterApplicationsView.as_view(), name="recruit-view"),
    path("jobseekerview/",MyApplicationsView.as_view(), name="jobseeker-view"),
    path("updatestatus/<int:app_id>/",UpdateApplicationStatus.as_view(), name="update-status"),
    
]