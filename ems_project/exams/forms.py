from django import forms
from .models import ExamResult
from students.models import StudentProfile

class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['student', 'subject', 'exam_name', 'obtained_marks', 'total_marks', 'grade']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'exam_name': forms.Select(attrs={'class': 'form-control'}),
            'obtained_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        subject_instance = kwargs.pop('subject_instance', None)
        super().__init__(*args, **kwargs)
        if subject_instance:
            self.fields['student'].queryset = StudentProfile.objects.filter(courses=subject_instance)
        self.fields['total_marks'].initial = 100
