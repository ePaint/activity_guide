from django.shortcuts import render
from categories.models import Category


def home(request):
    categories = Category.objects.filter(is_active=True, parent=None)[:3]
    context = {
        'categories': categories,
    }
    return render(request, 'categories/home.html', context)

def detail(request, slug):
    category = Category.objects.get(slug=slug)
    # activities = category.activities.all().order_by('-created_at')
    activities = category.get_activities().order_by('-created_at')
    providers = set()
    for activity in activities:
        providers.add(activity.provider)
    context = {
        'category': category,
        'activities': activities,
        'providers': providers,
    }
    return render(request, 'categories/detail.html', context)