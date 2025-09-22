from django.db import models
from users.models import User
from courses.models import Course  

# Attendance Models

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='student_attendance')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='teacher_attendance')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # changed from subject=CharField
    date = models.DateField()

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.course.name} - {self.status}"

