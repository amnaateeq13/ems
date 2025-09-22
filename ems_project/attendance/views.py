from users.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Attendance
from .forms import AttendanceForm
from students.models import StudentProfile
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from attendance.models import Attendance
from parents.models import ParentProfile
from courses.models import Course

#------------------------ Attendance View ------------------------
@login_required
def attendance_list_view(request):
   
    return render(request, 'attendance/attendance_list.html', {})

#------------------------ Admin Attendance View subject list  ------------------------
@login_required
@role_required('admin')
def admin_attendance_subject_list(request):
    subjects = Course.objects.all()
    return render(request, 'attendance/admin_subject_list.html', {'subjects': subjects})

#------------------------ Admin Attendance View Subject Report------------------------
@login_required
@role_required('admin')
def admin_subject_attendance_report(request, course_id):
    course = Course.objects.get(pk=course_id)
    records = Attendance.objects.filter(course=course).order_by('date')

    return render(request, 'attendance/admin_subject_report.html', {
        'course': course,
        'records': records,
    })

#------------------------ Teacher Attendance Mark ------------------------
@login_required
@role_required('teacher')
def mark_attendance(request):
    teacher = request.user
    students = User.objects.filter(studentprofile__courses__teacher=teacher).distinct()

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        form.fields['student'].queryset = students
        if form.is_valid():
            try:
                attendance = form.save(commit=False)
                attendance.teacher = teacher
                attendance.save()
                messages.success(request, 'Attendance marked successfully.')
                return redirect('mark_attendance')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Invalid form. Please correct the errors.')
    else:
        form = AttendanceForm()
        form.fields['student'].queryset = students

    return render(request, 'attendance/mark_attendance.html', {'form': form})

#------------------------ Teacher Attendance Subject View ------------------------

@login_required
@role_required('teacher')
def teacher_subjects_view(request):
    teacher = request.user
    from courses.models import Course
    courses = Course.objects.filter(teacher=teacher)
    return render(request, 'attendance/teacher_subjects.html', {'courses': courses})


#------------------------ Teacher Attendance Upload ------------------------

@login_required
@role_required('teacher')
def upload_attendance(request, course_id):
    from courses.models import Course
    from students.models import StudentProfile

    teacher = request.user
    course = Course.objects.get(pk=course_id, teacher=teacher)
    students = User.objects.filter(student_profile__courses=course)


    if request.method == 'POST':
        date = request.POST.get('date')
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    teacher=teacher,
                    date=date,
                    course=course,
                    defaults={'status': status}
                )
        messages.success(request, 'Attendance uploaded successfully.')
        return redirect('teacher_subjects')
    
    return render(request, 'attendance/upload_attendance.html', {
        'students': students,
        'course': course,
    })


#------------------------ Teacher Attendance View ------------------------
@login_required
@role_required('teacher')
def view_attendance(request, course_id):
    from courses.models import Course
    course = Course.objects.get(pk=course_id)
    records = Attendance.objects.filter(course=course).order_by('-date')
    return render(request, 'attendance/view_attendance.html', {'records': records, 'course': course})



#------------------------ Student Attendance View ------------------------
@login_required
@role_required('student')
def student_attendance_view(request):
    records = Attendance.objects.filter(student=request.user).order_by('-date')
    return render(request, 'attendance/student_attendance.html', {'records': records})

#------------------------ Student Attendance Subject wise  ------------------------
@login_required
@role_required('student')
def student_subjects_view(request):
    student = request.user
    subjects = student.student_profile.courses.all()  
    return render(request, 'attendance/student_subjects.html', {'subjects': subjects})

#------------------------ Student Attendance Subject wise detail ------------------------

@login_required
@role_required('student')
def student_subject_attendance_detail(request, course_id):
    student = request.user
    course = Course.objects.get(pk=course_id)
    records = Attendance.objects.filter(student=student, course=course)

    total = records.count()
    present = records.filter(status='present').count()
    absent = records.filter(status='absent').count()
    late = records.filter(status='late').count()

    def get_percent(value):
        return round((value / total) * 100, 2) if total else 0

    context = {
        'course': course,
        'records': records,
        'total': total,
        'present_percent': get_percent(present),
        'absent_percent': get_percent(absent),
        'late_percent': get_percent(late),
    }
    return render(request, 'attendance/student_attendance_detail.html', context)


#------------------------ Parent Attendance View ------------------------
@login_required
@role_required('parent')
def parent_attendance_view(request):
    try:
        parent_profile = ParentProfile.objects.get(user=request.user)
        
        children = parent_profile.children.all()

        
        records = Attendance.objects.filter(student__in=[child.user for child in children]).order_by('-date')
    except ParentProfile.DoesNotExist:
        records = []

    return render(request, 'attendance/parent_attendance.html', {
        'records': records,
        'children': children if 'children' in locals() else [],
    })



from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


