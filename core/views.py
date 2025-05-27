from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import Student, Teacher 
from django.contrib import messages
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")
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


from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from collections import defaultdict
from django.shortcuts import render
from .models import Grade


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def student_dashboard(request):
    student = request.user.student
    grades = Grade.objects.filter(student=student).order_by('year_level', 'semester', 'course')

    grouped_grades = defaultdict(lambda: defaultdict(list))
    for g in grades:
        # Use .strip() to avoid whitespace issues
        year = g.year_level.strip()
        semester = g.semester.strip()
        grouped_grades[year][semester].append(g)

    # Convert defaultdict to regular dict for template safety
    grouped_grades = {year: dict(semesters) for year, semesters in grouped_grades.items()}

 
    return render(request, 'student_dashboard.html', {
        'grades': grades,
        'all_grades': grades,  
        'grouped_grades': grouped_grades,  # IMPORTANT: pass grouped_grades to template
    })

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
        course = request.POST['course']
        grade_value = request.POST['grade']
        year_level = request.POST['year_level']
        semester = request.POST['semester']
        
        student_obj = Student.objects.get(id=student_id)
        
        
        teacher = request.user.teacher
        
        Grade.objects.create(
            student=student_obj,
            course=course,
            grade=grade_value,
            year_level=year_level,
            semester=semester,
            teacher=teacher
        )
        messages.success(request, "Grade added successfully!")
        return redirect('teacher_dashboard')
    return redirect('login')

from django.shortcuts import get_object_or_404, redirect

@login_required
def edit_grade(request, grade_id):
    if hasattr(request.user, 'teacher'):
        grade = get_object_or_404(Grade, id=grade_id)
        if request.method == 'POST':
            grade.grade = request.POST['grade']
            grade.save()
            messages.success(request, "Grade updated successfully!")
            return redirect('teacher_dashboard')
        return render(request, 'edit_grade.html', {'grade': grade})
    return redirect('login')

@login_required
def delete_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == "POST":
        grade.delete()
        messages.success(request, "Grade deleted successfully.")
        return redirect('teacher_dashboard')
    return redirect('teacher_dashboard') 

from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')  





