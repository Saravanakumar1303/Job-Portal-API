from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import JobApplication
from job.models import Job
from .serializers import JobApplicationSerializer

# Create your views here.
class JobApplyAPIView(APIView):
    permission_classes =[IsAuthenticated]

    def post(self, request):
        
        if request.user.role !='jobseeker':
            return Response({"message":"Only jobseekers can apply the job"},status=status.HTTP_403_FORBIDDEN)
        
        job_id = request.data.get("job")
        if not job_id:
            return Response({"error":"job is required."},status=status.HTTP_400_BAD_REQUEST)
        
        job = get_object_or_404(Job, id=job_id)

        if JobApplication.objects.filter(applicant=request.user, job=job).exists():
            return Response({"error":"You have already apply this job"},status=status.HTTP_400_BAD_REQUEST)
        
        application = JobApplication.objects.create(applicant=request.user, job=job)
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Recruiter Views own job application
class RecruiterApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'recruiter':
            return Response({"error": "Not allowed"}, status=403)

        applications = JobApplication.objects.filter(job__company=request.user)
        data = [
            {
                "job": app.job.title,
                "applicant": app.applicant.username,
                "status": app.status
            }
            for app in applications
        ]

        return Response(data)
    
# Jobseeker view own applications
class MyApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = JobApplication.objects.filter(applicant=request.user)
        data = [
            {
                "job": app.job.title,
                "status": app.status
            }
            for app in applications
        ]

        return Response(data)
    
# Recruiter Can Change the applicant status
class UpdateApplicationStatus(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, app_id):
        application = JobApplication.objects.get(id=app_id)

        if request.user != application.job.company:
            return Response({"error": "Not allowed"}, status=403)

        application.status = request.data.get("status")
        application.save()

        return Response({"message": "Status updated"})