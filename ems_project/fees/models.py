
from django.db import models
from datetime import date
from users.models import User

class Fee(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='fees'
    )
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField(default=date.today().year)
    date_generated = models.DateField(default=date.today)  
    due_date = models.DateField(null=True, blank=True)     
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.annual_fee} ({self.status}) - {self.year}"
