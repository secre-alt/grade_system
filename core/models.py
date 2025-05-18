# core/models.py
from django.contrib.auth.models import User
from django.db import models

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"Teacher: {self.user.username}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade_level = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.CharField(max_length=255)
    grade = models.CharField(max_length=5)
    year_level = models.CharField(
        max_length=10,
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year'),
        ]
    )
    semester = models.CharField(
        max_length=10,
        choices=[
            ('1st Sem', '1st Sem'),
            ('2nd Sem', '2nd Sem'),
        ]
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.course} - {self.student.user.username}: {self.grade}"
