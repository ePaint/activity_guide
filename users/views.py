from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from activities.models import Activity
from members.models import Member
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, UserUpdateForm, UserProfileImageForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect


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
            auth_login(request, user)
            response = HttpResponse()
            response.headers['HX-Trigger'] = 'reload-page'
            return response
    else:
        form = UserRegisterForm()
    
    extra_htmls = [
        'You already have an account? <a class="btn d-inline rounded orange-hover" role="button" data-bs-target="#modal_global" hx-get="/users/login/" hx-trigger="click" hx-target="#modal_global">Login</a>',
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
                'onclick': f'window.open("{activity.url}")',
            })
    
    extra_htmls = [
        'You don\'t have an account? <a class="btn d-inline rounded orange-hover" role="button" data-bs-target="#modal_global" hx-get="/users/register/" hx-trigger="click" hx-target="#modal_global">Register</a>',
        'Forgot your password? <a class="btn d-inline rounded orange-hover" role="button" data-bs-target="#modal_global" hx-get="/users/password-reset/" hx-trigger="click" hx-target="#modal_global">Reset password</a>'
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
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)


def password_reset(request):
    extra_buttons = []
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            ...
    else:
        form = PasswordResetForm()
    
    extra_htmls = [
        'You don\'t have an account? <a class="btn d-inline rounded orange-hover" role="button" data-bs-target="#modal_global" hx-get="/users/register/" hx-trigger="click" hx-target="#modal_global">Register</a>',
    ]
    context = {
        'form': form,
        'extra_htmls': extra_htmls,
        'extra_buttons': extra_buttons,
        'title': 'Reset your password',
        'submit_label': 'Reset password',
        'endpoint': request.path,
        'close_on_submit': False,
    }
    return render(request, 'layout/partials/form.html', context)


class UserPasswordResetView(PasswordResetView):
    template_name = "layout/partials/form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_htmls = [
            'You don\'t have an account? <a class="btn d-inline rounded orange-hover" role="button" data-bs-target="#modal_global" hx-get="/users/register/" hx-trigger="click" hx-target="#modal_global">Register</a>',
        ]
        extra_buttons = []

        context.update({
            'extra_htmls': extra_htmls,
            'extra_buttons': extra_buttons,
            'title': 'Reset your password',
            'submit_label': 'Reset password',
            'endpoint': self.request.path,
            'close_on_submit': False,
        })

        return context
    

def password_reset_done(request):
    messages = [
        {
            'text': 'We\'ve sent you an email with instructions on how to reset your password. Please check your inbox.',
            'type': 'success',
        }
    ]
    context = {
        'title': 'Reset your password',
        'submit_label': 'Accept',
        'messages': messages,
        'close_on_submit': True,
    }
    return render(request, 'layout/partials/form.html', context)


class UserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'submit_label': 'Reset password',
            'endpoint': self.request.path,
            'close_on_submit': False,
        })

        return context


def password_reset_complete(request):
    messages = [
        {
            'text': 'Your password has been successfully reset. You can now log in with your new password.',
            'type': 'success',
        }
    ]
    context = {
        'messages': messages,
        'title': 'Password reset complete',
        'submit_label': 'Go to login',
        'endpoint': '/users/login/',
        'method': 'get',
        'close_on_submit': False,
    }
    return render(request, 'layout/partials/form.html', context)


