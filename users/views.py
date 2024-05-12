from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import resolve
from activities.models import Activity
from layout.decorators import login_required

from members.models import Member
from providers.models import Provider
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
            member.liked_activities.set(Activity.objects.all().order_by('?')[:5])
            member.save()
            auth_login(request, user)
            response = HttpResponse()
            response.headers['HX-Trigger'] = 'reload-page'
            return response
    else:
        form = UserRegisterForm()
    
    extra_htmls = [
        f'You already have an account? <a class="btn d-inline rounded orange-hover" role="button" data-bs-target="#modal_global" hx-get="/users/login/" hx-trigger="click" hx-target="#modal_global">Login</a>',
    ]
    
    context = {
        'form': form,
        'extra_htmls': extra_htmls,
        'title': 'Create an account',
        'submit_label': 'Sign Up',
        'endpoint': request.path,
        'close_on_submit': False,
    }
    return render(request, 'layout/partials/form.html', context)


def login(request):
    extra_buttons = []
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
                response = HttpResponse()
                response.headers['HX-Trigger'] = 'reload-page'
                return response
    else:
        form = UserLoginForm()
        if 'target_activity' in request.GET:
            activity = Activity.objects.get(slug=request.GET['target_activity'])
            extra_buttons.append({
                'label': 'Continue as Guest',
                'color': 'orange',
                'onclick': f'window.open("{activity.provider.url}")',
            })
    
    extra_htmls = [
        f'You don\'t have an account? <a class="btn d-inline rounded orange-hover" role="button" data-bs-target="#modal_global" hx-get="/users/register/" hx-trigger="click" hx-target="#modal_global">Register</a>',
    ]
    context = {
        'form': form,
        'extra_htmls': extra_htmls,
        'extra_buttons': extra_buttons,
        'title': 'Login to your account',
        'submit_label': 'Sign In',
        'endpoint': request.path,
        'close_on_submit': False,
    }
    return render(request, 'layout/partials/form.html', context)


def logout(request):
    auth_logout(request)
    response = HttpResponse()
    response['HX-Redirect'] = '/'
    response.headers['HX-Trigger'] = 'reload-page'
    return response


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            response = render(request, 'users/profile.html', context)
            response.headers['HX-Trigger'] = 'reload-navbar'
            return response
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)

def profile_image_update(request):
    if request.method == 'POST':
        form = UserProfileImageForm(request.POST, instance=request.user.profile)
        print(form.is_valid())
        print(form.errors)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)
