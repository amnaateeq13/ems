
from django.contrib import admin
from .models import Subject, Exam, ExamResult


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher')
    search_fields = ('name', 'code')
    list_filter = ('teacher',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'date')
    search_fields = ('title',)
    list_filter = ('subject', 'date')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'subject', 'exam_name', 'obtained_marks', 'total_marks', 'percentage', 'grade', 'date')
    list_filter = ('exam_name', 'subject', 'grade')
    search_fields = ('student__user__username', 'exam_name', 'subject__name')
