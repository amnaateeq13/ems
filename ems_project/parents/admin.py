from django.contrib import admin
from .models import ParentProfile

class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'parent_id', 'contact_number']
    filter_horizontal = ['children']  # For ManyToMany field

admin.site.register(ParentProfile, ParentProfileAdmin)
