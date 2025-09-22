from django.contrib import admin
from .models import TimeSlot, TimeTable

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')
    list_filter = ('start_time', 'end_time')

from .forms import TimeTableForm

@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    form = TimeTableForm
    list_display = ('day', 'class_name', 'section', 'course', 'teacher', 'room', 'time_slot')
    list_filter = ('day', 'class_name', 'teacher')
    search_fields = ('class_name', 'section', 'course__name', 'teacher__username', 'room')

