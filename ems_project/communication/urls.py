

from .views import (
    announcement_list_view,
    create_announcement_view,
    edit_announcement_view,
    delete_announcement_view,
    teacher_announcement_list_view,   
    teacher_announcement_create_view,
)
from .views import role_chat_view , fetch_messages_ajax , chat_history_view

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("api/", include(router.urls)),
    path('', announcement_list_view, name='announcements'),
    path('create/', create_announcement_view, name='create_announcement'),
    path('edit/<int:pk>/', edit_announcement_view, name='edit_announcement'),
    path('delete/<int:pk>/', delete_announcement_view, name='delete_announcement'),

    path('teacher/', teacher_announcement_list_view, name='teacher_announcements'),
    path('teacher/create/', teacher_announcement_create_view, name='teacher_create_announcement'),


    
    path('chat/', role_chat_view, name='role_chat'),
    path('admin/chat/fetch/<int:receiver_id>/', fetch_messages_ajax, name='fetch_messages_ajax'),
    path('chat/history/', chat_history_view, name='chat_history'),


]
