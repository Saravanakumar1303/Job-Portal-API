from job.models import Job
from rest_framework import serializers

class JobSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    class Meta:
        model = Job
        fields = ['id','title','description','location','salary','company','created_at']
        read_only_fields = ['company','created_at']

    def get_company(self, obj):
        return f"{obj.company.first_name} {obj.company.last_name}"

