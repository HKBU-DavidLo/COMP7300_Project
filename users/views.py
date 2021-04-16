from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        #profileform = ProfileForm(request.POST)
        if form.is_valid():  # and profileform.is_valid():
            form.save()
            # profileform.save
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            #mobile = profileform.cleaned_data.get('mobile')
            # print(mobile)

            messages.success(
                request, f'Account created for {username}!')
            # models.Profile.objects.create(mobile=form.cleaned_data.get('mobile'))
            return redirect('profile')
    else:
        form = UserRegisterForm()
        #profileform = ProfileForm()

    # , 'profileform': profileform})
    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(
            request.POST, instance=request.user.profile)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form
    }
    return render(request, 'users/profile.html', context)
