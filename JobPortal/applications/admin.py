from applications.models import JobApplication
from django.contrib import admin

@admin.register(JobApplication)
class JobApplyAdmin(admin.ModelAdmin):
    list_display =['id','applicant','job','status','applied_at']