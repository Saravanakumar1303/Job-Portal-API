from rest_framework import serializers
from .models import JobApplication
from job.models import Job
from job.serializers import JobSerializer

class JobApplicationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    job = serializers.PrimaryKeyRelatedField(
        queryset =Job.objects.all(),
        write_only = True
    )
    
    job_details = JobSerializer(source = 'job',read_only=True)
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applicant','status']
