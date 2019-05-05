from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Major, StudentProfile, StudentCareer

admin.site.register(CustomUser)
admin.site.register(Major)
admin.site.register(StudentProfile)
admin.site.register(StudentCareer)
