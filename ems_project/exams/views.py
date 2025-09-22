from django.contrib.auth import get_user_model
from .models import Exam, Subject, ExamResult
from parents.models import ParentProfile
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import ExamResult
from users.decorators import role_required
from .forms import ExamResultForm
from students.models import StudentProfile
from exams.models import ExamResult
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import Subject, Exam

@login_required
def exam_list(request):
    user = request.user
    if user.role == 'parent':
        return redirect('exams:parent_exam_results')
    
    if user.role == 'teacher':
        subjects = Course.objects.filter(teacher=user)

    elif user.role == 'student':
        student_subjects = user.student_profile.courses.all()
        subjects = student_subjects

    else:  
        subjects = Course.objects.all()

    exams = Exam.objects.filter(subject__in=subjects).order_by('date')

    return render(request, 'exams/exam_list.html', {
        'subjects': subjects,
        'exams': exams
    })


@login_required
def exam_results_view(request):
    if request.user.role == 'student':
        results = ExamResult.objects.filter(student__user=request.user).order_by('-date')
    elif request.user.role == 'parent':
        results = ExamResult.objects.filter(student__user__parentprofile__user=request.user).order_by('-date')
    else:
        results = ExamResult.objects.all().order_by('-date')
    return render(request, 'exams/exam_results.html', {'results': results})



@login_required
@role_required('teacher')
def upload_exam_result(request):
    subject_id = request.GET.get('subject')
    subject = get_object_or_404(Course, id=subject_id)

    enrolled_students = StudentProfile.objects.filter(courses=subject)

    if request.method == 'POST':
        form = ExamResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.teacher = request.user.teacherprofile
            result.subject = subject.name
            result.total_marks = 100  
            result.percentage = (result.obtained_marks / result.total_marks) * 100

            
            if result.percentage >= 90:
                result.grade = 'A+'
            elif result.percentage >= 80:
                result.grade = 'A'
            elif result.percentage >= 70:
                result.grade = 'B'
            elif result.percentage >= 60:
                result.grade = 'C'
            elif result.percentage >= 50:
                result.grade = 'D'
            else:
                result.grade = 'F'

            
            existing = ExamResult.objects.filter(
                student=result.student,
                subject=result.subject,
                exam_name=result.exam_name
            ).first()

            if existing and not request.POST.get('overwrite'):
                messages.warning(request, "This result already exists. Click Submit again to overwrite it.")
                return render(request, 'exams/upload_exam_result.html', {
                    'form': form,
                    'subject': subject,
                    'existing': True
                })

            elif existing and request.POST.get('overwrite'):
               
                existing.obtained_marks = result.obtained_marks
                existing.percentage = result.percentage
                existing.grade = result.grade
                existing.teacher = result.teacher
                existing.save()
                messages.success(request, "Result successfully updated.")
                return redirect('exams:exam_list')

            else:
                result.save()
                messages.success(request, "Result successfully uploaded.")
                return redirect('exams:exam_list')
    else:
        form = ExamResultForm(initial={'subject': subject.name})

    return render(request, 'exams/upload_exam_result.html', {
        'form': form,
        'subject': subject,
        'existing': False
    })




@login_required
@role_required('student')
def student_subject_list(request):
    student = request.user.student_profile
    subjects = student.courses.all()
    return render(request, 'exams/student_subjects.html', {'subjects': subjects})



@login_required
@role_required('student')
def subject_result_detail(request, subject_id):
    student = request.user.student_profile
    subject = get_object_or_404(Course, id=subject_id)
    results = ExamResult.objects.filter(student=student, subject=subject.name)
    return render(request, 'exams/subject_result_detail.html', {
        'subject': subject,
        'results': results,
    })



@login_required
@role_required('student')
def student_exam_results(request):
    student = request.user.studentprofile
    results = ExamResult.objects.filter(student=student)
    return render(request, 'exams/student_exam_results.html', {'results': results})






@login_required
@role_required('parent')
def parent_exam_results(request):
    parent_profile = request.user.parent_profile

    
    children = StudentProfile.objects.filter(parents=parent_profile)


    results = ExamResult.objects.filter(student__in=children).select_related(
        'student__user',  
        'teacher'         
    )

    return render(request, 'exams/parent_exam_results.html', {
        'results': results
    })







@login_required
@role_required('teacher') 
def view_results_by_subject(request, subject_id):
    subject = get_object_or_404(Course, id=subject_id)
    results = ExamResult.objects.filter(subject=subject.name).order_by('-date')
    
    return render(request, 'exams/view_subject_results.html', {
        'subject': subject,
        'results': results,
    })




def manage_exam(request):
    subjects = Subject.objects.all()
    exams = Exam.objects.all()
    return render(request, 'exams/manage_exam.html', {'subjects': subjects, 'exams': exams})

def search_exam_ajax(request):
    query = request.GET.get('q', '').strip()

    subjects = Subject.objects.all()
    exams = Exam.objects.all()

    if query:
        subjects = subjects.filter(Q(name__icontains=query) | Q(code__icontains=query))
        exams = exams.filter(
            Q(title__icontains=query) |
            Q(subject__name__icontains=query) |
            Q(subject__code__icontains=query) |
            Q(date__icontains=query)
        )

    html = render_to_string('exams/exam_table_body.html', {
        'subjects': subjects,
        'exams': exams
    })
    return JsonResponse({'html': html})

from rest_framework import viewsets
from .models import ExamResult
from .serializers import ExamResultSerializer

class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
