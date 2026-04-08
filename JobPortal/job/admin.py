from django.contrib import admin
from job.models import Job
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','location','salary','company','created_at']