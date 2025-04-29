from django.contrib import admin
from .models import Teacher, Student

# Register your models here.

admin.site.site_header = "School Admin Dashboard"
admin.site.site_title = "Grade System Admin"
admin.site.index_title = "Welcome to the Admin Portal"

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade_level')
