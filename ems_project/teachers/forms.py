from django import forms
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import TeacherProfile
User = get_user_model()

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        exclude = ['employee_id']
        fields = [ 'employee_id', 'department', 'subject_specialization', 'qualification', 'contact_number', 'profile_picture']



User = get_user_model()

class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    department = forms.CharField(label='Department')
    subject_specialization = forms.CharField(label='Subject Specialization')
    qualification = forms.CharField(label='Qualification')
    contact_number = forms.CharField(label='Contact Number')

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'confirm_password',
            'department', 'subject_specialization', 'qualification', 'contact_number'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
