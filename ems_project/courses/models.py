from django.db import models
from users.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})
    
    def __str__(self):
        return f"{self.name} ({self.code})"
