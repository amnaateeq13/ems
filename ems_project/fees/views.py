from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Fee
from .forms import FeeForm
from users.models import User
from parents.models import ParentProfile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Fee
from students.models import StudentProfile
@login_required
def fee_list(request):
    role = request.user.role
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

 
    if role == 'admin':
        fees = Fee.objects.all()
        if query:
            fees = fees.filter(
                Q(student__username__icontains=query) |
                Q(student__student_profile__roll_number__icontains=query) |
                Q(student__student_profile__class_name__icontains=query) |
                Q(year__icontains=query)
            )
        if status_filter:
            fees = fees.filter(status=status_filter)

        return render(request, 'fees/fee_list.html', {'fees': fees})


    elif role == 'teacher':
        fees = Fee.objects.all()  # Teachers can see all fees
        if query:
            fees = fees.filter(
                Q(student__username__icontains=query) |
                Q(student__student_profile__roll_number__icontains=query) |
                Q(student__student_profile__class_name__icontains=query) |
                Q(year__icontains=query)
            )
        if status_filter:
            fees = fees.filter(status=status_filter)

        return render(request, 'fees/teacher_fee_list.html', {'fees': fees})


    elif role == 'student':
        fees = Fee.objects.filter(student=request.user)
        if query:
            fees = fees.filter(
                Q(student__username__icontains=query) |
                Q(student__student_profile__roll_number__icontains=query) |
                Q(student__student_profile__class_name__icontains=query) |
                Q(year__icontains=query)
            )
        if status_filter:
            fees = fees.filter(status=status_filter)

        return render(request, 'fees/student_fee_list.html', {'fees': fees})


    elif role == 'parent':
        try:
            parent_profile = request.user.parent_profile
            children = StudentProfile.objects.filter(parents=parent_profile)
            fees = Fee.objects.filter(student__in=[child.user for child in children])

            if query:
                fees = fees.filter(
                    Q(student__username__icontains=query) |
                    Q(student__student_profile__roll_number__icontains=query) |
                    Q(student__student_profile__class_name__icontains=query) |
                    Q(year__icontains=query)
                )
            if status_filter:
                fees = fees.filter(status=status_filter)

            return render(request, 'fees/parent_fee_list.html', {'fees': fees})
        except ParentProfile.DoesNotExist:
            return render(request, 'fees/parent_fee_list.html', {'fees': []})


@login_required
def fee_create(request):
    if request.user.role != 'admin':
        return redirect('fee_list')

    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fee_list')
    else:
        form = FeeForm()

    students = User.objects.filter(role='student').select_related('student_profile')
    return render(request, 'fees/fee_create.html', {'form': form, 'students': students})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeeForm
from .models import Fee
from django.contrib.auth.decorators import login_required

@login_required
def fee_edit(request, pk):
    fee = get_object_or_404(Fee, pk=pk)

    if request.user.role != 'admin':
        return redirect('fee_list')

    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            return redirect('fee_list')  
    else:
        form = FeeForm(instance=fee)

    return render(request, 'fees/fee_edit.html', {'form': form, 'fee': fee})


@login_required
def fee_delete(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.user.role == 'admin':
        fee.delete()
    return redirect('fee_list')



from django.shortcuts import render, get_object_or_404
from .models import Fee
from django.contrib.auth.decorators import login_required

@login_required
def fee_voucher(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    return render(request, 'fees/fee_voucher.html', {'fee': fee})


from rest_framework import viewsets
from .models import Fee
from .serializers import FeeSerializer

class FeeRecordViewSet(viewsets.ModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
