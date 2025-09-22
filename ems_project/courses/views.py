from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course
from django.shortcuts import render, get_object_or_404, redirect
import random
import string
from .models import Course
from .forms import CourseForm
from .forms import CourseForm
from users.decorators import role_required
import re
@login_required
def course_list_view(request):
    if request.user.role == 'teacher':
        courses = Course.objects.filter(teacher=request.user)
    else:
        courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def generate_next_course_code(prefix="CS"):
    
    courses = Course.objects.filter(code__startswith=prefix).order_by('-code')
    
    if not courses.exists():
        return f"{prefix}101"

    last_code = courses.first().code  # e.g., CSE105
    match = re.match(rf"{prefix}(\d+)", last_code)
    
    if match:
        number = int(match.group(1)) + 1
        return f"{prefix}{number}"
    else:
        return f"{prefix}101"

@login_required
@role_required('admin')
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully.")
            return redirect('course_list')
    else:
        initial_code = generate_next_course_code("CS")  
        form = CourseForm(initial={'code': initial_code})
    
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
@role_required('admin')
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course'})

@login_required
@role_required('admin')
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


from django.shortcuts import render, get_object_or_404, redirect
from users.models import User
from .models import Course
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import role_required

@login_required
@role_required('admin')
def allocate_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    teachers = User.objects.filter(role='teacher')

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        selected_teacher = get_object_or_404(User, id=teacher_id, role='teacher')
        course.teacher = selected_teacher
        course.save()
        messages.success(request, f"{course.name} successfully allocated to {selected_teacher.get_full_name()}")
        return redirect('course_list')

    return render(request, 'courses/allocate_course.html', {
        'course': course,
        'teachers': teachers,
    })

from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
