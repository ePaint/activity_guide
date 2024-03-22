from django.shortcuts import render
from categories.models import Category
from layout.views import _paginate


def home(request):
    categories = Category.objects.filter(is_active=True, parent=None)[:3]
    context = {
        'categories': categories,
    }
    return render(request, 'categories/home.html', context)

def detail(request, slug):
    category = Category.objects.get(slug=slug)
    activities = category.get_activities().order_by('-updated_at')
    providers = set()
    for activity in activities:
        providers.add(activity.provider)
    
    providers, next_page = _paginate(list(providers), request.GET.get('page'))
    
    context = {
        'category': category,
        'providers': providers,
        'next_page': next_page,
    }
    return render(request, 'categories/detail.html', context)