from django.shortcuts import render


def member_profile(request):
    return render(request, 'members/member_profile.html')


def member_dashboard(request):
    return render(request, 'members/member_dashboard.html')