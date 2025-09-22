
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TeacherProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from users.models import User
from users.decorators import role_required
from django.contrib import messages
from .forms import TeacherForm
from .models import TeacherProfile, generate_teacher_id

User = get_user_model()

@login_required
@role_required('admin')
def teacher_list_view(request):
    teachers = User.objects.filter(role='teacher')
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

@login_required
def teacher_profile_view(request):
    try:
        profile = TeacherProfile.objects.get(user=request.user)
        return render(request, 'teachers/teacher_profile.html', {'profile': profile})
    except TeacherProfile.DoesNotExist:
        return render(request, 'teachers/teacher_profile.html', {'profile': None})

@login_required
@role_required('teacher')
def teacher_dashboard(request):
    teacher_profile = request.user.teacherprofile  
    context = {
        'teacher': teacher_profile,
       
    }
    return render(request, 'users/teacher_dashboard.html', context)

@login_required
@role_required('teacher')
def update_teacher_profile(request):
    profile, created = TeacherProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherProfileForm(instance=profile)

    return render(request, 'teachers/update_teacher_profile.html', {'form': form})


@login_required
@role_required('admin')
def delete_teacher_view(request, teacher_id):
    teacher = get_object_or_404(User, id=teacher_id, role='teacher')
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully.')
        return redirect('teacher_list')
    return render(request, 'teachers/confirm_delete_teacher.html', {'teacher': teacher})

@login_required
@role_required('admin')
def edit_teacher(request, username):
    teacher_user = get_object_or_404(User, username=username, role='teacher')
    teacher_profile, created = TeacherProfile.objects.get_or_create(user=teacher_user)

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher profile updated successfully.')
            return redirect('manage_teachers')
    else:
        form = TeacherProfileForm(instance=teacher_profile)

    return render(request, 'teachers/edit_teacher.html', {'form': form, 'teacher': teacher_user})

@login_required
@role_required('admin')
def delete_teacher(request, username):
    teacher = get_object_or_404(User, username=username, role='teacher')
    
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully.')
        return redirect('manage_teachers')
    
    return render(request, 'teachers/confirm_delete_teacher.html', {'teacher': teacher})

@login_required
@role_required('admin')
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'teacher'
            user.set_password(form.cleaned_data['password'])  
            user.save()

            TeacherProfile.objects.create(
                user=user,
                employee_id=generate_teacher_id(),  
                department='Not Assigned',
                subject_specialization='Not Assigned'
            )

            messages.success(request, 'Teacher added successfully.')
            return redirect('manage_teachers')
    else:
        form = TeacherForm()
    return render(request, 'teachers/add_teacher.html', {'form': form})


from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from users.models import User

def manage_teachers(request):
    teachers = User.objects.filter(role='teacher')
    return render(request, 'teachers/manage_teachers.html', {'teachers': teachers})

def search_teachers_ajax(request):
    query = request.GET.get('q', '').strip()
    teachers = User.objects.filter(role='teacher')

    if query:
        teachers = teachers.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(teacherprofile__employee_id__icontains=query) |
            Q(teacherprofile__qualification__icontains=query) |
            Q(teacherprofile__department__icontains=query) |
            Q(teacherprofile__subject_specialization__icontains=query)
        )

    html = render_to_string('teachers/teacher_table_body.html', {'teachers': teachers})
    return JsonResponse({'html': html})


from rest_framework import viewsets
from .models import TeacherProfile
from .serializers import TeacherSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherSerializer
