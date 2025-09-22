from django.urls import path, include

from .views import teacher_profile_view, update_teacher_profile
from .views import teacher_list_view
from .views import add_teacher
from . import views
from .views import edit_teacher, delete_teacher
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet
router = DefaultRouter()
router.register(r"teachers", TeacherViewSet, basename="teacher")
urlpatterns = [
    path("api/", include(router.urls)),
    path('', teacher_list_view, name='manage_teachers'),
    path('profile/', teacher_profile_view, name='teacher_profile'),
    path('update_teacher_profile/', views.update_teacher_profile, name='update_teacher_profile'),
    path('add/', add_teacher, name='add_teacher'),
    path('edit/<str:username>/', edit_teacher, name='edit_teacher'),  
    path('delete/<str:username>/', delete_teacher, name='delete_teacher'),  
 



    path('manage-teachers/', views.manage_teachers, name='manage_teachers'),
    path('search-teachers/', views.search_teachers_ajax, name='search_teachers_ajax'),


]
