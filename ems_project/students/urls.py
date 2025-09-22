from django.urls import path,include
from .views import add_student, edit_student, delete_student, student_list_view, student_profile_view
from . import views
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")



urlpatterns = [
    path('api/', include(router.urls)),
    path('', student_list_view, name='manage_students'),
    path('add/', add_student, name='add_student'),
    path('edit/<str:roll_number>/', edit_student, name='edit_student'),
    path('delete/<str:roll_number>/', delete_student, name='delete_student'),
    path('profile/', student_profile_view, name='student_profile'),
    path('manage-students/', views.manage_students1, name='manage_students1'),
    path('search-students/', views.search_students_ajax, name='search_students_ajax'),
]
