from django.shortcuts import render
from providers.models import Provider


def provider_profile(request, slug):
    provider = Provider.objects.get(slug=slug)
    context = {
        'provider': provider,
    }
    return render(request, 'providers/provider_profile.html', context)
