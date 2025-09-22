
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet

router = DefaultRouter()
router.register(r"attendance", AttendanceViewSet, basename="attendance")
urlpatterns = [
    path("api/", include(router.urls)),
    # Teacher relevant usrls
    path('', views.teacher_subjects_view, name='teacher_subjects'),
    path('<int:course_id>/upload/', views.upload_attendance, name='upload_attendance'),
    path('<int:course_id>/view/', views.view_attendance, name='view_attendance'),

    # Admin relevant urls
    path('admin/reports/', views.admin_attendance_subject_list, name='admin_attendance_subject_list'),
    path('admin/reports/<int:course_id>/', views.admin_subject_attendance_report, name='admin_subject_attendance_report'),

    #parent relevant urls
    path('parent/', views.parent_attendance_view, name='parent_attendance'),

    #student relevant urls
    path('student/subjects/', views.student_subjects_view, name='student_subjects'),
    path('student/attendance/<int:course_id>/', views.student_subject_attendance_detail, name='student_attendance_detail'),


]