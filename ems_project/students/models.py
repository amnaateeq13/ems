from django.db import models
from users.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='student_profile'
    )
    
    roll_number = models.CharField(max_length=20, blank=False, null=False)

    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    allocated_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'teacher'})
    courses = models.ManyToManyField(
        'courses.Course',
        related_name='enrolled_students',
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"
