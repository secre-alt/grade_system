from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('add-grade/', views.add_grade, name='add_grade'),
    path('edit-grade/<int:grade_id>/', views.edit_grade, name='edit_grade'),
    path('delete-grade/<int:grade_id>/', views.delete_grade, name='delete_grade'),
]
