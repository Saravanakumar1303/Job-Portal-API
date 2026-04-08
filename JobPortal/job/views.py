from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from job.models import Job
from .serializers import JobSerializer
from .permissions import IsRecruiter

# Create your views here.
class JobListAPIView(APIView):
    permission_classes = [IsRecruiter,IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = JobSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(company = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class JobUpdateAPIView(APIView):
    permission_classes = [IsRecruiter]

    def get_object(self, request, pk):
        return get_object_or_404(Job, pk=pk, company = request.user)
    
    def put(self,request,pk):
        jobs = self.get_object(request,pk)
        serializer = JobSerializer(jobs, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request,pk):
        jobs = self.get_object(request, pk)
        serializer = JobSerializer(jobs, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDeleteAPIView(APIView):
    permission_classes = [IsRecruiter]

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        job.delete()
        return Response({"message":"Job Deleted Successfully."},status=status.HTTP_200_OK)
    