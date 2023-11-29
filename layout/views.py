from django.shortcuts import render


def not_found(request, exception):
    print(f'404 error')
    return render(request, 'layout/404.html')


def server_error(request):
    print(f'500 error')
    return render(request, 'layout/500.html')


def base(request):
    return render(request, 'layout/base.html')


def home(request):
    return render(request, 'layout/home.html')


def about(request):
    return render(request, 'layout/about.html')


def contact(request):
    return render(request, 'layout/contact.html')


def categories(request):
    return render(request, 'layout/categories.html')


def navbar(request):
    return render(request, 'layout/navbar.html')
