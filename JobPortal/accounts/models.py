from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICE =(
        ("jobseeker", "Job_Seeker"),
        ("recruiter", "Recruiter"),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default="jobseeker")
    profile_photo = models.ImageField(upload_to="profile_photos/",blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    
class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    resume = models.FileField(upload_to='resumes/')
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} Resume"