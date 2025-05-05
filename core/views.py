from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import Student, Teacher 

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Check role
            if hasattr(user, 'student'):
                return redirect('student_dashboard')  # Replace with your student dashboard URL name
            elif hasattr(user, 'teacher'):
                return redirect('teacher_dashboard')  # Replace with your teacher dashboard URL name
            elif user.is_superuser:
                return redirect('/admin/')  # Admin site
            else:
                messages.error(request, 'Unknown role.')
                return redirect('login')

        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Grade

@login_required
def student_dashboard(request):
    if hasattr(request.user, 'student'):
        student = request.user.student
        grades = Grade.objects.filter(student=student)
        return render(request, 'student_dashboard.html', {'grades': grades})
    return redirect('login')

@login_required
def teacher_dashboard(request):
    if hasattr(request.user, 'teacher'):
        teacher = request.user.teacher
        students = Student.objects.all()
        grades = Grade.objects.filter(teacher=teacher)
        return render(request, 'teacher_dashboard.html', {'students': students, 'grades': grades})
    return redirect('login')

@csrf_exempt
@login_required
def add_grade(request):
    if hasattr(request.user, 'teacher') and request.method == 'POST':
        student_id = request.POST['student_id']
        subject = request.POST['subject']
        grade_value = request.POST['grade']
        student = Student.objects.get(id=student_id)
        teacher = request.user.teacher
        Grade.objects.create(
            student=student,
            subject=subject,
            grade=grade_value,
            teacher=teacher
        )
        return redirect('teacher_dashboard')
    return redirect('login')

@login_required
def edit_grade(request, grade_id):
    if hasattr(request.user, 'teacher'):
        grade = get_object_or_404(Grade, id=grade_id)
        if request.method == 'POST':
            grade.subject = request.POST['subject']
            grade.grade = request.POST['grade']
            grade.save()
            return redirect('teacher_dashboard')
        return render(request, 'edit_grade.html', {'grade': grade})
    return redirect('login')

@login_required
def delete_grade(request, grade_id):
    if hasattr(request.user, 'teacher'):
        grade = get_object_or_404(Grade, id=grade_id)
        grade.delete()
        return redirect('teacher_dashboard')
    return redirect('login')

