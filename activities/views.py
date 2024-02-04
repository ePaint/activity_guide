from django.http import HttpResponse
from django.shortcuts import render
from django.urls import resolve
from django.core.exceptions import ValidationError
from activities.models import FORM_MAPPER, Activity
from layout.views import field_edit


def activity_detail(request, slug):
    activity = Activity.objects.get(slug=slug)
    context = {
        'activity': activity
    }
    return render(request, 'activities/view.html', context)

def activity_edit(request, slug):
    activity = Activity.objects.get(slug=slug)
    context = {
        'activity': activity
    }
    return render(request, 'activities/edit.html', context)

def activity_field_edit(request, pk, field):
    return field_edit(request, Activity, 'activity', pk, field, FORM_MAPPER[field])

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
        
    return render(request, 'activities/partials/like.html', {'activity': activity})
