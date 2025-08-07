from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict

from core.models import Student, Teacher, Grade

# Utility functions for role checks
def is_teacher(user):
    return hasattr(user, 'teacher')

def is_student(user):
    return hasattr(user, 'student')

# Home View
def home(request):
    return render(request, 'core/home.html')

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")

            if is_student(user):
                return redirect('student_dashboard')
            elif is_teacher(user):
                return redirect('teacher_dashboard')
            elif user.is_superuser:
                return redirect('admin:index')
            else:
                messages.error(request, 'Unknown role.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

# Student Dashboard
@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = request.user.student
    grades = Grade.objects.filter(student=student).order_by('year_level', 'semester', 'course')

    grouped_grades = defaultdict(lambda: defaultdict(list))
    for g in grades:
        year = g.year_level.strip()
        semester = g.semester.strip()
        grouped_grades[year][semester].append(g)

    grouped_grades = {year: dict(semesters) for year, semesters in grouped_grades.items()}

    return render(request, 'student_dashboard.html', {
        'grades': grades,
        'all_grades': grades,
        'grouped_grades': grouped_grades,
    })

# Teacher Dashboard
@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = request.user.teacher
    students = Student.objects.all()
    grades = Grade.objects.filter(teacher=teacher)
    return render(request, 'teacher_dashboard.html', {
        'students': students,
        'grades': grades
    })

# Add Grade
@csrf_exempt
@login_required
@user_passes_test(is_teacher)
def add_grade(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        course = request.POST['course']
        grade_value = request.POST['grade']
        year_level = request.POST['year_level']
        semester = request.POST['semester']

        student_obj = get_object_or_404(Student, id=student_id)
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

# Edit Grade
@login_required
@user_passes_test(is_teacher)
def edit_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == 'POST':
        grade.grade = request.POST['grade']
        grade.save()
        messages.success(request, "Grade updated successfully!")
        return redirect('teacher_dashboard')
    return render(request, 'edit_grade.html', {'grade': grade})

# Delete Grade
@login_required
@user_passes_test(is_teacher)
def delete_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == "POST":
        grade.delete()
        messages.success(request, "Grade deleted successfully.")
        return redirect('teacher_dashboard')
    return render(request, 'confirm_delete.html', {'grade': grade})
