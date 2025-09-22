from django.db import models
from students.models import StudentProfile
from users.models import User
from teachers.models import TeacherProfile
from courses.models import Course  


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return self.name


class Exam(models.Model):
    subject = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.subject.name})"





class ExamResult(models.Model):
    EXAM_TYPE_CHOICES = [
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('assignment', 'Assignment'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    exam_name = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    total_marks = models.PositiveIntegerField()
    obtained_marks = models.PositiveIntegerField(null=True, blank=True)
    percentage = models.FloatField(blank=True, null=True)
    grade = models.CharField(max_length=2, blank=True)

    def save(self, *args, **kwargs):
        if self.total_marks > 0:
            self.percentage = (self.obtained_marks / self.total_marks) * 100
            if self.percentage >= 90:
                self.grade = 'A+'
            elif self.percentage >= 80:
                self.grade = 'A'
            elif self.percentage >= 70:
                self.grade = 'B'
            elif self.percentage >= 60:
                self.grade = 'C'
            elif self.percentage >= 50:
                self.grade = 'D'
            else:
                self.grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject} ({self.exam_name})"

   
    class Meta:
        unique_together = ('student', 'subject', 'exam_name')
