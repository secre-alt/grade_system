from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/add-grade/', views.add_grade, name='add_grade'),
]
