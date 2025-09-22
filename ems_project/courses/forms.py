# courses/forms.py
from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'teacher']
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'Auto-generated or enter manually'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter course name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Course description'}),
        }

    def clean_code(self):
        code = self.cleaned_data['code']
        if Course.objects.filter(code=code).exists():
            raise forms.ValidationError("This course code already exists.")
        return code
