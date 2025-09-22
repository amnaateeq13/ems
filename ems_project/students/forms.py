from django import forms
from django.core.exceptions import ValidationError
from users.models import User
from .models import StudentProfile
from courses.models import Course

class StudentForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()  
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    allocated_teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(role='teacher'),
        required=False
    )

    class Meta:
        model = StudentProfile
        fields = ['class_name', 'section', 'courses', 'allocated_teacher']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")

        if username and User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")

        return cleaned_data

    def save(self, commit=True):
        student_profile = super().save(commit=False)

      
        user = self.instance.user if self.instance and hasattr(self.instance, 'user') else User()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.role = 'student'

      
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        if commit:
            user.save()
            student_profile.user = user

            if not student_profile.roll_number:
                last = StudentProfile.objects.order_by('-id').first()
                next_number = int(last.roll_number[3:]) + 1 if last and last.roll_number.startswith("stu") else 1
                student_profile.roll_number = f"stu{next_number:04d}"

            student_profile.save()
            self.save_m2m()

        return student_profile
