from django.shortcuts import render


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
