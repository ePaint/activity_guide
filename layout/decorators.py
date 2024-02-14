from django.shortcuts import redirect


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('layout-home')
        return view_func(request, *args, **kwargs)
    return wrapper


def provider_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_provider:
            return redirect('layout-home')
        return view_func(request, *args, **kwargs)
    return wrapper