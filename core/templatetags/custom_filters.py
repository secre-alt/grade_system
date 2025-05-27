from django import template

register = template.Library()

@register.filter
def floatval(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

@register.filter
def calculate_gpa(grades):
    try:
        grade_values = [float(g.grade) for g in grades if g.grade is not None]
        if not grade_values:
            return "N/A"
        gpa = sum(grade_values) / len(grade_values)
        return f"{gpa:.2f}"
    except:
        return "N/A"

@register.filter
def flatten_grades(semesters):
    grades = []
    for semester_grades in semesters:
        grades.extend(semester_grades)
    return grades

