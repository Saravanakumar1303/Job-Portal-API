from django.db import models
from django.conf import settings
from job.models import Job

# Create your models here.  
user = settings.AUTH_USER_MODEL

class JobApplication(models.Model):
    STATUS_CHOICES =[
        ('applied','Applied'),
        ('reviewed','Reviewed'),
        ('shortlisted','Shortlisted'),
        ('rejected','Rejected')
    ]
    applicant = models.ForeignKey(user, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['applicant','job']
        ordering = ['-applied_at']
        
    def __str__(self):
        return f"{self.applicant} applied for {self.job}"
