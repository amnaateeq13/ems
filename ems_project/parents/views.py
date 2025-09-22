from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from .models import ParentProfile
from .forms import ParentUserForm, ParentProfileForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from students.models import StudentProfile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from students.models import StudentProfile
from courses.models import Course
from attendance.models import Attendance
from communication.models import Announcement

# ----- List View -----
@login_required
@role_required('admin')
def parent_list_view(request):
    parents = ParentProfile.objects.select_related('user').prefetch_related('children')
    return render(request, 'parents/parent_list.html', {'parents': parents})

# ----- Add Parent View -----
@login_required
@role_required('admin')
def add_parent_view(request):
    if request.method == 'POST':
        user_form = ParentUserForm(request.POST)
        profile_form = ParentProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save(commit=False)
            user.role = 'parent'

            
            password = user_form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

           
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.parent_id = ParentProfile.generate_parent_id()
            profile.save()
            profile_form.save_m2m() 

            return redirect('parent_list')
    else:
        user_form = ParentUserForm()
        profile_form = ParentProfileForm()

    return render(request, 'parents/add_parent.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


# ----- Edit Parent View -----
@login_required
@role_required('admin')
def edit_parent_view(request, pk):
    parent = get_object_or_404(ParentProfile, pk=pk)
    user = parent.user

    if request.method == 'POST':
       
        user_form = ParentUserForm(request.POST, instance=user)
        profile_form = ParentProfileForm(request.POST, instance=parent)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('parent_list')

    else:
       
        user_form = ParentUserForm(instance=user)
        profile_form = ParentProfileForm(instance=parent)

    return render(request, 'parents/edit_parent.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'parent': parent
    })


# ----- Delete Parent View -----
@login_required
@role_required('admin')
def delete_parent_view(request, pk):
    parent = get_object_or_404(ParentProfile, pk=pk)

    if request.method == 'POST':
        
        parent.user.delete()
        return redirect('parent_list')

    return render(request, 'parents/delete_parent.html', {'parent': parent})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from parents.models import ParentProfile

@login_required
@role_required('parent')
def parent_profile_view(request):
    parent_profile = request.user.parent_profile 
    children = parent_profile.children.all()     

    context = {
        'parent_profile': parent_profile,
        'children': children
    }
    return render(request, 'parents/parent_profile.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from .models import ParentProfile
from .forms import ParentProfileUpdateForm

@login_required
@role_required('parent')
def update_parent_profile(request):
    parent_profile = request.user.parent_profile

    if request.method == 'POST':
        form = ParentProfileUpdateForm(request.POST, request.FILES, instance=parent_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('parent_profile')  
    else:
        form = ParentProfileUpdateForm(instance=parent_profile)

    return render(request, 'parents/update_parent_profile.html', {'form': form})

from rest_framework import viewsets
from .models import ParentProfile
from .serializers import ParentSerializer

class ParentViewSet(viewsets.ModelViewSet):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentSerializer
