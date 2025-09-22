from django.db import models
from users.models import User

def generate_teacher_id():
    last_profile = TeacherProfile.objects.order_by('-id').first()
    if last_profile and last_profile.employee_id.startswith('faculty'):
        last_id = int(last_profile.employee_id.replace('faculty', ''))
        new_id = last_id + 1
    else:
        new_id = 1
    return f"faculty{new_id:04d}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    employee_id = models.CharField(max_length=20, editable=False)
    department = models.CharField(max_length=100)
    subject_specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, default='Not specified')
    contact_number = models.CharField(max_length=20, default='0000000000')
    profile_picture = models.ImageField(upload_to='teacher_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"
