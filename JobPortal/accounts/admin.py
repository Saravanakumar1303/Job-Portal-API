from django.contrib import admin
from accounts.models import User,Resume
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =("first_name","last_name","email","role","profile_photo","created_at")
    list_filter =("first_name","email","created_at")

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("user","resume","skills","experience","updated_at")