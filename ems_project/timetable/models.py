
from django.db import models
from users.models import User
from courses.models import Course

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

class TimeTable(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    class_name = models.CharField(max_length=50)  # e.g., BSCS 5th
    section = models.CharField(max_length=10, blank=True, null=True)
    room = models.CharField(max_length=20)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('day', 'time_slot', 'room')  # Avoid room conflicts

    def __str__(self):
        return f"{self.class_name} - {self.course.name} ({self.day})"
