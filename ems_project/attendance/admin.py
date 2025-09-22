from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'status', 'teacher']

    list_filter = ['date', 'status']
