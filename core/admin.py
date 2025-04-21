from django.contrib import admin
from .models import CustomUser, Grade, StudentProfile, TeacherProfile
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Grade)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)