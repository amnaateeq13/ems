from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'created_by', 'audience']
    list_filter = ['created_at', 'audience']
