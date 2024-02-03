from django.http import HttpResponse
from django.shortcuts import render
from django.urls import resolve
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

def activity_like(request, slug):
    if not request.user.is_authenticated:
        view = resolve('/users/login/').func
        request.method = 'GET'
        response = view(request)
        response.headers['HX-Retarget'] = '.main-content'
        response.headers['HX-Push-Url'] = '/users/login/?next=' + request.GET.get('next', '/')
        return response
    
    member = request.user.member
    activity = Activity.objects.get(slug=slug)

    if member.liked_activities.filter(slug=slug).exists():
        member.liked_activities.remove(activity)
    else:
        member.liked_activities.add(activity)
        
    return render(request, 'activities/partials/activity_like.html', {'activity': activity})
