from django.shortcuts import render
from activities.models import Activity


def activity_detail(request, slug):
    activity = Activity.objects.get(slug=slug)
    context = {
        'activity': activity
    }
    return render(request, 'activities/activity_detail.html', context)
