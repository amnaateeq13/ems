
from .views import course_list_view
from . import views
from .views import allocate_course
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
urlpatterns = [
    path("api/", include(router.urls)),
    path('', course_list_view, name='course_list'),
    path('add/', views.add_course, name='add_course'),
    path('edit/<int:pk>/', views.edit_course, name='edit_course'),
    path('delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('allocate/<int:course_id>/', allocate_course, name='allocate_course'),

]
