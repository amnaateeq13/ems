from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from users.decorators import role_required
from .models import StudentProfile
from .forms import StudentForm
from users.models import User
from .forms import StudentForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q



@login_required
def student_profile_view(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
        return render(request, 'students/student_profile.html', {'profile': profile})
    except StudentProfile.DoesNotExist:
        return render(request, 'students/student_profile.html', {'profile': None})



@login_required
@role_required('admin')
def student_list_view(request):
    students = StudentProfile.objects.select_related('user').all()
    return render(request, 'students/student_list.html', {'students': students})




@login_required
@role_required('admin')
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_students')  
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})


@login_required
@role_required('admin')
def edit_student(request, roll_number):
    student = StudentProfile.objects.get(roll_number=roll_number)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('manage_students')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/edit_student.html', {
    'form': form,
    'student': student  
})


@login_required
@role_required('admin')
def delete_student(request, roll_number):
    student = StudentProfile.objects.get(roll_number=roll_number)
    if request.method == 'POST':
        student.user.delete()  
        student.delete()       
        messages.success(request, 'Student deleted successfully.')
        return redirect('manage_students')
    return render(request, 'students/delete_student.html', {'student': student})




def manage_students1(request):
    students = StudentProfile.objects.all()
    return render(request, 'students/manage_students1.html', {'students': students})

def search_students_ajax(request):
    query = request.GET.get('q', '').strip()
    students = StudentProfile.objects.all()

    if query:
        students = students.filter(
            Q(roll_number__icontains=query) |
            Q(class_name__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query) |
            Q(allocated_teacher__first_name__icontains=query) |
            Q(allocated_teacher__last_name__icontains=query)
        )

    html = render_to_string('students/student_table_body.html', {'students': students})
    return JsonResponse({'html': html})


from rest_framework import viewsets
from .models import StudentProfile
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentSerializer
