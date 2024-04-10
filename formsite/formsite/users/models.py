from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from appforms.models import AppForm

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/users/profile_photos/',verbose_name="Profile Photo", blank=True)
    bio = models.TextField(max_length=100, blank=True)
    my_forms = models.ManyToManyField(AppForm, blank=True, related_name='my_forms')
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "User Profiles"
