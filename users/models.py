from django.db import models
from django.contrib.auth.models import User
from .forms import UserRegisterForm


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30, blank=True)
    mobile = models.CharField(
        max_length=15, help_text='Enter your area code and mobile no., e.g. for HK mobile, +85291231234', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
