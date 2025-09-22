from django.db import models
from django.conf import settings
from users.models import User


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    AUDIENCE_CHOICES = (
        ('all', 'All'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )

    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES)

    def __str__(self):
        return self.title


class AnnouncementRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')

from django.db import models
from users.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.content[:20]}"
