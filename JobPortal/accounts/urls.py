from django.urls import path
from accounts.views import *

urlpatterns =[
    path("register/",RegisterView.as_view(), name="register"),
    path("login/",LoginView.as_view(), name="login"),
    path("logout/",LogoutAPIView.as_view(), name="logout"),
    path("profile/",ProfileAPIView.as_view(), name="profile-view"),
    path("uploadresume/",ResumeUploadAPIView.as_view(), name="upload-resume"),
]