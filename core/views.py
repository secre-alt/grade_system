from django.shortcuts import render
from .models import Grade, StudentProfile
from django.contrib.auth.decorators import login_required

# Create your views here.

def input_grade(request):
    if request.user.role != 'teacher':
        return redirect('home')
    
    students = StudentProfile.objects.all()
    if request.method == 'POST':
        student_id = request.POST['student']
        subject = request.POST['subject']
        grade = request.POST['grade']

        student = StudentProfile.objects.get(id=student_id)
        Grade.objects.create(student=student, subject=subject, grade=grade)
        return redirect('input_grade')
    
    return render(request, 'core/input_grade.html', 
                  {'students': students})