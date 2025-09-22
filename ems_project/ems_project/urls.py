"""
URL configuration for ems_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView
schema_view = get_schema_view(
   openapi.Info(
      title="EMS Project API",
      default_version="v1",
      description="API documentation for the Education Management System",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="support@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('student/', include('students.urls')),
    path('teacher/', include('teachers.urls')),
    path('parent/', include('parents.urls')),
    path('courses/', include('courses.urls')),
    path('attendance/', include('attendance.urls')),
    path('exams/', include('exams.urls')),
    path('announcements/', include('communication.urls')),
    path('fees/', include('fees.urls')),
    path('timetable/', include('timetable.urls')),

     # Swagger & ReDoc
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('api-links/', TemplateView.as_view(template_name="api_endpoints.html"), name="api-endpoints"),
    
]