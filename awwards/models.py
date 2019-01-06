from __future__ import unicode_literals

from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    dp = models.ImageField(upload_to='images')
    bio = HTMLField(max_length=300)
    phone_number = models.BigIntegerField()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def __str__(self):
        return self.user.username
