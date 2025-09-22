from django.db import models
from users.models import User
from students.models import StudentProfile

class ParentProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'parent'},
        related_name='parent_profile'
    )
    parent_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    children = models.ManyToManyField('students.StudentProfile', blank=True, related_name='parents')
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='parent_pics/', blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} - {self.parent_id}"

    @staticmethod
    def generate_parent_id():
        last_parent = ParentProfile.objects.order_by('id').last()
        if not last_parent:
            return "parent0001"
        last_id = int(last_parent.parent_id.replace("parent", ""))
        return f"parent{last_id+1:04d}"
