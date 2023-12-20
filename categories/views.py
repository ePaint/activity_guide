from django.shortcuts import render
from categories.models import Category


def home(request):
    categories = Category.objects.all().order_by('created_at')[:3]
    context = {
        'categories': categories,
    }
    return render(request, 'categories/home.html', context)

def detail(request, slug):
    category = Category.objects.get(slug=slug)
    offers = category.offer_set.all().order_by('-created_at')
    providers = set()
    for offer in offers:
        providers.add(offer.provider)
    context = {
        'category': category,
        'offers': offers,
        'providers': providers,
    }
    return render(request, 'categories/detail.html', context)