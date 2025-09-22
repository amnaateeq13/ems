# from django.contrib import admin
# from .models import FeeRecord

# @admin.register(FeeRecord)
# class FeeRecordAdmin(admin.ModelAdmin):
#     list_display = ('student', 'month', 'total_fee', 'amount_paid', 'due_date', 'payment_date', 'is_paid')
#     list_filter = ('month', 'due_date', 'payment_date')
from django.contrib import admin
from .models import Fee

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'annual_fee', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__username',)
