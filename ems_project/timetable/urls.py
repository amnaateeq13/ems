
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimetableViewSet

router = DefaultRouter()
router.register(r"timetables", TimetableViewSet, basename="timetable")

urlpatterns = [
    path("api/", include(router.urls)),
    path('admin-view/', views.admin_timetable, name='admin_timetable'),
  
    path('admin-add/', views.add_timetable, name='add_timetable'),


    path('teacher/', views.teacher_timetable, name='teacher_timetable'),
    path('parent/', views.parent_timetable, name='parent_timetable'),

    path('student/', views.student_timetable, name='student_timetable'),
]
