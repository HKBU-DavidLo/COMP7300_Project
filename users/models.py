from django.db import models
from django.contrib.auth.models import User
import random
#from .forms import UserRegisterForm


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30, blank=True)
    fund = models.FloatField(default=0.0)
    mobile = models.CharField(
        max_length=20, help_text='Enter your area code and mobile no., e.g. for HK mobile, +85291231234', blank=True)

    def __str__(self):
        return f'{self.user} Profile'


class Code(models.Model):
    number = models.CharField(max_length=6, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(6):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.number = code_string

        super().save(*args, **kwargs)
