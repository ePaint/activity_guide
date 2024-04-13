from django.shortcuts import render
from ads.models import get_ads_by_location
from categories.models import Category
from layout.views import _paginate


def home(request):
    categories = Category.objects.filter(is_active=True, parent=None)[:3]
    context = {
        'categories': categories,
        'ads_1': get_ads_by_location('C1'),
        'ads_2': get_ads_by_location('C2'),
        'ads_3': get_ads_by_location('C3'),
    }
    return render(request, 'categories/home.html', context)

def detail(request, slug):
    category = Category.objects.get(slug=slug)
    root_category = category.get_root_category()
    
    if root_category.slug == 'art':
        ads = get_ads_by_location('ARTS')
    elif root_category.slug == 'sports':
        ads = get_ads_by_location('SPORTS')
    else:
        ads = get_ads_by_location('STEM')
    
    activities = category.get_activities().order_by('-updated_at')
    providers = set()
    for activity in activities:
        providers.add(activity.provider)
    
    providers, next_page = _paginate(list(providers), request.GET.get('page'))
    
    context = {
        'category': category,
        'providers': providers,
        'next_page': next_page,
        'ads': ads,
    }
    print('context:', context)
    return render(request, 'categories/detail.html', context)