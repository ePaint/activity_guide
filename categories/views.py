from django.shortcuts import render
from categories.models import Category


def home(request):
    categories = Category.objects.all().order_by('created_at')[:3]
    return render(request, 'categories/home.html', {'categories': categories})

def detail(request, slug):
    category = Category.objects.get(slug=slug)
    offers = category.offer_set.all().order_by('-created_at')
    return render(request, 'categories/detail.html', {'category': category, 'offers': offers})