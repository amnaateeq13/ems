from django import forms
from .models import Attendance
from users.models import User


#Attendnce Form
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
