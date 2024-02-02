from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError
from activities.models import Activity


def activity_detail(request, slug):
    activity = Activity.objects.get(slug=slug)
    context = {
        'activity': activity
    }
    return render(request, 'activities/activity_detail.html', context)

def activity_edit(request, slug):
    activity = Activity.objects.get(slug=slug)
    context = {
        'activity': activity
    }
    return render(request, 'activities/activity_edit.html', context)

def activity_field_edit(request, slug):
    if (request.method != 'POST'):
        return HttpResponse('')
    field = request.POST.get('field')
    value = request.POST.get('value')
    prev_value = request.POST.get('prev_value')
    activity = Activity.objects.get(slug=slug)
    if (field not in activity.__dict__):
        return HttpResponse(prev_value)
    
    activity.__dict__[field] = value

    try:
        activity.save()
    except ValidationError:
        return HttpResponse(prev_value)
    
    return HttpResponse(value)
    