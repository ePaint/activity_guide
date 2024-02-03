from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import resolve
from activities.models import Activity

from members.models import Member
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, UserUpdateForm, UserProfileImageForm
from .models import User, UserProfile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_member = True
            user.is_provider = False
            user.save()
            member = Member(user=user)
            member.save()
            print(member)
            print('Creating member...')
            member.liked_activities.set(Activity.objects.all().order_by('?')[:5])
            print(member)
            print('Creating liked activities...')
            member.save()
            return redirect('users-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                auth_login(request, user)
                redirect_path = form.cleaned_data.get('next')
                next = resolve(redirect_path)
                print('next:', next)
                response = next.func(request, *next.args, **next.kwargs)
                response.headers['HX-Trigger'] = 'reloadNavBar'
                response.headers['HX-Replace-Url'] = redirect_path
                return response
    else:
        print(request.GET)
        initial = {
            'next': request.GET.get('next', '/'),
        }
        form = UserLoginForm(initial=initial)
    return render(request, 'users/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    response = render(request, 'users/logout.html')
    response.headers['HX-Trigger'] = 'reloadNavBar'
    response.headers['HX-Replace-Url'] = '/users/logout/'
    return response


@login_required
def profile(request):
    if request.method == 'POST':
        image_form = UserProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'image_form': image_form,
        }
        if user_form.is_valid() and profile_form.is_valid():
            image_form.save()
            user_form.save()
            profile_form.save()

            response = render(request, 'users/profile.html', context)
            response.headers['HX-Trigger'] = 'reloadNavBar'
            return response
    else:
        image_form = UserProfileImageForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'image_form': image_form,
    }
    return render(request, 'users/profile.html', context)

