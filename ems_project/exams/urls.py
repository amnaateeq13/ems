
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamResultViewSet

router = DefaultRouter()
router.register(r"exams", ExamResultViewSet, basename="examresult")

app_name = 'exams'

urlpatterns = [
    path("api/", include(router.urls)),
    # Exam dashboard/list
    path('', views.exam_list, name='exam_list'),

    # Upload & manage exams
    path('upload/', views.upload_exam_result, name='upload_exam_result'),
    path('manage-exam/', views.manage_exam, name='manage_exam'),
    path('search-exam/', views.search_exam_ajax, name='search_exam_ajax'),

    # Student-side views
    path('student-subjects/', views.student_subject_list, name='student_subjects'),
    path('student/subjects/<int:subject_id>/results/', views.subject_result_detail, name='subject_result_detail'),

    # Subject-wise result view (for teachers/admin)
    path('subject/<int:subject_id>/results/', views.view_results_by_subject, name='view_results_by_subject'),

    #  Parent exam results view
    path('parent-results/', views.parent_exam_results, name='parent_exam_results'),
]
