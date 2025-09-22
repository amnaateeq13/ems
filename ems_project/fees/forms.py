from django import forms
from .models import Fee

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['student', 'annual_fee', 'year', 'date_generated', 'due_date', 'status']
        widgets = {
            'date_generated': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
