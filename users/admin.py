from django.contrib import admin
from .models import Profile, Code
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
# admin.site.register(Code)
#admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fund', 'email', 'mobile']


# admin.site.register(Code)


@admin.register(Code)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'number']
