from django.shortcuts import render
from categories.models import Category
from offers.models import Offer


def not_found(request, exception):
    print(f'404 error')
    return render(request, 'layout/404.html')


def server_error(request):
    print(f'500 error')
    return render(request, 'layout/500.html')


def not_ready(request):
    print(f'Not ready')
    return render(request, 'layout/not_ready.html')


def base(request):
    return render(request, 'layout/base.html')


def home(request):
    categories = Category.objects.all().order_by('created_at')[:3]
    return render(request, 'layout/home.html', {'categories': categories})


def navbar(request):
    return render(request, 'layout/navbar.html')


def search_results(request):
    offers = Offer.objects.all()
    context = {
        'offers': offers
    }
    return render(request, 'layout/search_results.html', context)
