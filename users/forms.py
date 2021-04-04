from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm (UserCreationForm):
    email = forms.EmailField()
    mobile = forms.CharField(
        max_length=15, help_text='Enter your area code and mobile no., e.g. for HK mobile, +85291231234')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'mobile', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    mobile = forms.CharField(
        max_length=15, help_text='Enter your area code and mobile no., e.g. for HK mobile, +85291231234')

    class Meta:
        model = User
        fields = ['email', 'mobile']
