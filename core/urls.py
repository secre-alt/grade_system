from django.urls import path
from . import views

urlpatterns = [
    path('grades/', views.view_grades, name='view_grades'),
]
