from django.urls import path
from .views import (
    user_login, user_logout,
    admin_dashboard, teacher_dashboard,
    student_dashboard, parent_dashboard, home ,register
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('parent-dashboard/', parent_dashboard, name='parent_dashboard'),
]
