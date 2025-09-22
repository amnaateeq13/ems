from students.models import StudentProfile  
from .models import Announcement, AnnouncementRead
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Message
from .forms import MessageForm
from users.models import User
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils.timesince import timesince
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import AnnouncementForm
from .decorators import role_required

@login_required
def announcement_list_view(request):
    role = request.user.role
    query = request.GET.get('q')
    announcements = Announcement.objects.none()

    if role == 'admin':
        
        announcements = Announcement.objects.all()

    elif role == 'teacher':
        
        announcements = Announcement.objects.filter(
            Q(audience__in=["all", "teacher"]),
            created_by__role='admin'
        )

    elif role == 'student':
        student_profile = StudentProfile.objects.get(user=request.user)
        teacher_ids = User.objects.filter(course__in=student_profile.courses.all()).distinct()
        announcements = Announcement.objects.filter(
            Q(audience='all') |
            Q(audience='student', created_by__in=teacher_ids)
        )

    elif role == 'parent':
        parent_profile = getattr(request.user, 'parent_profile', None)
        if parent_profile:
            
            children = StudentProfile.objects.filter(parents=parent_profile)

            if children.exists():
                
                teacher_ids = User.objects.filter(
                    course__in=[c for child in children for c in child.courses.all()]
                ).distinct()

                announcements = Announcement.objects.filter(
                    Q(audience='all') |
                     Q(audience='parent', created_by__role='admin') |
                    Q(audience='parent', created_by__in=teacher_ids)
                    
                )


    if query:
        announcements = announcements.filter(
            Q(title__icontains=query) | Q(message__icontains=query)
        )
    
    for announcement in announcements:
        AnnouncementRead.objects.get_or_create(
            user=request.user,
            announcement=announcement
        )

    announcements = announcements.order_by('-created_at')
    return render(request, 'communication/announcement_list.html', {
        'announcements': announcements,
        'query': query,
    })


@login_required
@role_required('admin', 'teacher')  
def create_announcement_view(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            
            if request.user.role == 'teacher' and announcement.audience not in ['student', 'parent']:
                return HttpResponseForbidden("Teachers can only post to students or parents.")
            announcement.save()
            return redirect('announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'communication/create_announcement.html', {'form': form})





@login_required
@role_required('admin')
def edit_announcement_view(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully.")
            return redirect('announcements')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'communication/edit_announcement.html', {'form': form})

@login_required
@role_required('admin')
def delete_announcement_view(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, created_by=request.user)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, "Announcement deleted successfully.")
        return redirect('announcements')
    return render(request, 'communication/confirm_delete.html', {'announcement': announcement})







@login_required
@role_required('teacher')
def teacher_announcement_list_view(request):
   
    announcements = Announcement.objects.filter(
        Q(audience__in=["all", "teacher"]),
        created_by__role='admin'  
    ).order_by('-created_at')
    
    my_announcements = Announcement.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    return render(request, 'communication/teacher_announcement_list.html', {
        'announcements': announcements,
        'my_announcements': my_announcements,
    })


@login_required
@role_required('teacher')
def teacher_announcement_create_view(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, user=request.user)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            
            if announcement.audience not in ['student', 'parent']:
                return HttpResponseForbidden("You may only post to students or parents.")
            announcement.save()
            return redirect('teacher_announcements')
    else:
        form = AnnouncementForm(user=request.user)

    return render(request, 'communication/teacher_create_announcement.html', {
        'form': form
    })




@login_required
def role_chat_view(request):
    user = request.user
    role = user.role
    selected_role = request.GET.get('role')  
    receiver_id = request.GET.get('receiver')
    users = []
    receiver = None
    messages = []

    
    if role == 'admin':
        if selected_role:
            users = User.objects.filter(role=selected_role)
        receiver = User.objects.filter(id=receiver_id, role=selected_role).first() if receiver_id else None

   
    elif role == 'teacher':
        from students.models import StudentProfile
        from parents.models import ParentProfile

        
        users = list(User.objects.filter(role='admin'))

     
        student_profiles = StudentProfile.objects.filter(courses__in=user.course_set.all()).distinct()
        student_users = [s.user for s in student_profiles]
        users += student_users

       
        parent_profiles = ParentProfile.objects.filter(children__in=student_profiles).distinct()
        parent_users = [p.user for p in parent_profiles]
        users += parent_users

       
        receiver = User.objects.filter(id=receiver_id, id__in=[u.id for u in users]).first() if receiver_id else None

    elif role == 'student':
        from students.models import StudentProfile
        from parents.models import ParentProfile

        student_profile = StudentProfile.objects.get(user=user)

        # Teachers of this student
        teachers = User.objects.filter(course__in=student_profile.courses.all()).distinct()
        users = list(teachers)

       
        users += list(User.objects.filter(role='admin'))

        
        parent_profiles = ParentProfile.objects.filter(children=student_profile)
        for parent_profile in parent_profiles:
            users.append(parent_profile.user)

        receiver = User.objects.filter(id=receiver_id, id__in=[u.id for u in users]).first() if receiver_id else None


   
    elif role == 'parent':
        from students.models import StudentProfile
        from parents.models import ParentProfile

        parent_profile = ParentProfile.objects.get(user=user)
        student_profile = StudentProfile.objects.filter(parents=parent_profile).first()
        users = list(User.objects.filter(role='admin')) 
        if student_profile:
            users.append(student_profile.user) 

      
            teachers = User.objects.filter(course__in=student_profile.courses.all()).distinct()
            users += list(teachers)

        receiver = User.objects.filter(id=receiver_id, id__in=[u.id for u in users]).first() if receiver_id else None


   
    if receiver:
        messages = Message.objects.filter(
            Q(sender=user, receiver=receiver) |
            Q(sender=receiver, receiver=user)
        ).order_by('timestamp')

       
        unread = messages.filter(receiver=user, read=False)
        unread.update(read=True)

   
    if request.method == 'POST' and receiver:
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = user
            msg.receiver = receiver
            msg.save()
            return redirect(f"{request.path}?role={selected_role}&receiver={receiver.id}")
    else:
        form = MessageForm()

    return render(request, 'communication/chat.html', {
        'form': form,
        'messages': messages,
        'role': role,
        'selected_role': selected_role,
        'users': users,
        'selected_user': receiver,
    })




@login_required
@role_required('admin')
def fetch_messages_ajax(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    data = [{
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%d %b %Y %H:%M'),
        'me': msg.sender == request.user
    } for msg in messages]

    return JsonResponse({'messages': data})

@login_required
def chat_history_view(request):
    user = request.user

  
    sent_to = Message.objects.filter(sender=user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=user).values_list('sender', flat=True)

    partner_ids = set(list(sent_to) + list(received_from))
    partners = User.objects.filter(id__in=partner_ids)

    chat_data = []
    for partner in partners:
        last_message = Message.objects.filter(
            Q(sender=user, receiver=partner) | Q(sender=partner, receiver=user)
        ).order_by('-timestamp').first()

        unread_count = Message.objects.filter(sender=partner, receiver=user, read=False).count()

        chat_data.append({
            'partner': partner,
            'last_message': last_message,
            'unread_count': unread_count
        })

    return render(request, 'communication/chat_history.html', {
        'chat_data': chat_data
    })


from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
