from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from users.models import User

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'parent':
                return redirect('parent_dashboard')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def home(request):
    return render(request, 'users/home.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



from courses.models import Course

@login_required
@role_required('admin')
def admin_dashboard(request):
    total_teachers = User.objects.filter(role='teacher').count()
    total_students = User.objects.filter(role='student').count()
    total_parents = User.objects.filter(role='parent').count()
    total_courses = Course.objects.count()
    total_announcements = Announcement.objects.count()

    context = {
        'total_teachers': total_teachers,
        'total_students': total_students,
        'total_parents': total_parents,
        'total_courses': total_courses,
        'total_announcements': total_announcements
    }
    return render(request, 'users/admin_dashboard.html', context)


from django.db.models import Count
from courses.models import Course
from students.models import StudentProfile
from communication.models import Announcement

@login_required
@role_required('teacher')
def teacher_dashboard(request):
    teacher = request.user

    total_courses = Course.objects.filter(teacher=teacher).count()
    total_students = StudentProfile.objects.filter(courses__teacher=teacher).distinct().count()

    announcements = Announcement.objects.filter(created_by=teacher).count()

    context = {
        'total_courses': total_courses,
        'total_students': total_students,
        'announcements': announcements,
    }
    return render(request, 'users/teacher_dashboard.html', context)


from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from students.models import StudentProfile
from attendance.models import Attendance
from communication.models import Announcement

@login_required
@role_required('student')
def student_dashboard(request):
    student_user = request.user

    # Get the StudentProfile
    student_profile = StudentProfile.objects.get(user=student_user)

    # Count courses
    total_courses = student_profile.courses.count()

    # Count attendance records — FIXED line
    total_attendance = Attendance.objects.filter(student=student_user).count()

    # Announcements visible to students and to all
    total_announcements = Announcement.objects.filter(audience__icontains='student').count() + Announcement.objects.filter(
    audience__icontains='all' ).count()


    context = {
        'total_courses': total_courses,
        'total_attendance': total_attendance,
        'total_announcements': total_announcements
    }
    return render(request, 'users/student_dashboard.html', context)



# from parents.models import ParentProfile

# @login_required
# @role_required('parent')
# def parent_dashboard(request):
#     parent_user = request.user

#     try:
#         parent_profile = ParentProfile.objects.get(user=parent_user)
#         children = StudentProfile.objects.filter(parentprofile=parent_profile)

#         total_children = children.count()
#         total_courses = sum(child.courses.count() for child in children)
#         total_attendance = Attendance.objects.filter(student__in=children).count()

#         total_announcements = Announcement.objects.filter(
#             target_roles__icontains='parent'
#         ).count() + Announcement.objects.filter(
#             target_roles__icontains='all'
#         ).count()

#     except ParentProfile.DoesNotExist:
#         total_children = total_courses = total_attendance = total_announcements = 0

#     context = {
#         'total_children': total_children,
#         'total_courses': total_courses,
#         'total_attendance': total_attendance,
#         'total_announcements': total_announcements,
#     }
#     return render(request, 'users/parent_dashboard.html', context)

from parents.models import ParentProfile
from students.models import StudentProfile
from attendance.models import Attendance
from communication.models import Announcement
from django.contrib.auth.decorators import login_required
from users.decorators import role_required

@login_required
@role_required('parent')
def parent_dashboard(request):
    parent_user = request.user

    try:
        parent_profile = ParentProfile.objects.get(user=parent_user)

        # ✅ Get all children of this parent
        children = StudentProfile.objects.filter(parents=parent_profile)

        # ✅ Calculate dashboard statistics
        total_children = children.count()
        total_courses = sum(child.courses.count() for child in children)
        total_attendance = Attendance.objects.filter(student__in=[c.user for c in children]).count()

        # ✅ Fix: Use "audience" instead of "target_roles"
        total_announcements = (
            Announcement.objects.filter(audience__icontains='parent').count() +
            Announcement.objects.filter(audience__icontains='all').count()
        )

    except ParentProfile.DoesNotExist:
        total_children = total_courses = total_attendance = total_announcements = 0

    context = {
        'total_children': total_children,
        'total_courses': total_courses,
        'total_attendance': total_attendance,
        'total_announcements': total_announcements,
    }
    return render(request, 'users/parent_dashboard.html', context)
