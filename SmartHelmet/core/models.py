from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    contactno = models.CharField(max_length=20, default='')
    user_image=models.URLField(null=True)
    def __str__(self):
        return self.user.username

class Data(models.Model):
    pulse = models.IntegerField(default=0)
    pressure = models.IntegerField(default=0)
    temp = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
