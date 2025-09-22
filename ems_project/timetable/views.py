from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TimeTable
from students.models import StudentProfile
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from parents.models import ParentProfile

@staff_member_required
def admin_timetable(request):
    """Display full timetable for admin with filters"""

  
    class_filter = request.GET.get('class')
    teacher_filter = request.GET.get('teacher')
    day_filter = request.GET.get('day')

    
    timetable = TimeTable.objects.all().order_by('day', 'time_slot__start_time')

   
    if class_filter:
        timetable = timetable.filter(class_name__icontains=class_filter)
    if teacher_filter:
        timetable = timetable.filter(teacher__username__icontains=teacher_filter)
    if day_filter:
        timetable = timetable.filter(day=day_filter)

    context = {
        'timetable': timetable,
        'class_filter': class_filter,
        'teacher_filter': teacher_filter,
        'day_filter': day_filter,
        'days': TimeTable.DAY_CHOICES,
    }
    return render(request, 'timetable/admin_timetable.html', context)


@login_required
def teacher_timetable(request):
    """Display timetable for the logged-in teacher"""
    if request.user.role != 'teacher':
        return render(request, '403.html')  

    timetable = TimeTable.objects.filter(teacher=request.user).order_by('day', 'time_slot__start_time')
    return render(request, 'timetable/teacher_timetable.html', {'timetable': timetable})


@login_required
def student_timetable(request):
    """Display timetable for the logged-in student"""
    if request.user.role != 'student':
        return render(request, '403.html') 

    student_profile = StudentProfile.objects.get(user=request.user)
    timetable = TimeTable.objects.filter(
        class_name=student_profile.class_name,
        section=student_profile.section
    ).order_by('day', 'time_slot__start_time')

    return render(request, 'timetable/student_timetable.html', {'timetable': timetable})


@login_required
def parent_timetable(request):
    """Display timetable for all children of the logged-in parent"""
    if request.user.role != 'parent':
        return render(request, '403.html')

    try:
        parent_profile = ParentProfile.objects.get(user=request.user)
        children = parent_profile.children.all()  

        
        child_timetables = []
        for child in children:
            timetable = TimeTable.objects.filter(
                class_name=child.class_name,
                section=child.section
            ).order_by('day', 'time_slot__start_time')

            child_timetables.append({
                'child': child,
                'timetable': timetable
            })

    except ParentProfile.DoesNotExist:
        child_timetables = []

    return render(request, 'timetable/parent_timetable.html', {
        'child_timetables': child_timetables
    })




from django.contrib import messages
from django.shortcuts import redirect
from .forms import TimeTableForm

@staff_member_required
def add_timetable(request):
    if request.method == 'POST':
        form = TimeTableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Timetable entry added successfully!")
            return redirect('admin_timetable')
    else:
        form = TimeTableForm()

    return render(request, 'timetable/add_timetable.html', {'form': form})

from rest_framework import viewsets
from .models import TimeTable
from .serializers import TimeTableSerializer

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
