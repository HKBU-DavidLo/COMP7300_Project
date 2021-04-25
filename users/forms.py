from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .models import Code


class UserRegisterForm (UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    mobile = forms.CharField(
        max_length=15, help_text='Enter your area code and mobile no., e.g. for HK mobile, +85291231234')

    class Meta:
        model = Profile
        fields = ['email', 'mobile']


class CodeForm(forms.ModelForm):
    number = forms.CharField(
        label='Code', help_text='Enter SMS verification code')

    class Meta:
        model = Code
        fields = ('number',)
