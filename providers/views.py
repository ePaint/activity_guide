from django.http import HttpResponse
from django.shortcuts import render
from providers.forms import ProviderNameForm, ProviderDescriptionForm
from providers.models import Provider


def provider_profile(request, slug):
    provider = Provider.objects.get(slug=slug)
    context = {
        'provider': provider,
    }
    return render(request, 'providers/provider_profile.html', context)


def provider_edit(request, slug):
    provider = Provider.objects.get(slug=slug)
    name_form = ProviderNameForm(instance=provider)
    description_form = ProviderDescriptionForm(instance=provider)
    context = {
        'provider': provider,
        'name_form': name_form,
        'description_form': description_form,
    }
    return render(request, 'providers/provider_edit.html', context)


def provider_name_update(request, slug):
    provider = Provider.objects.get(slug=slug)
    if request.method == 'POST':
        form = ProviderNameForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
    else:
        form = ProviderNameForm(instance=provider)
    return render(request, 'providers/provider_name_form.html', {'form': form})


def provider_description_update(request, slug):
    provider = Provider.objects.get(slug=slug)
    if request.method == 'POST':
        print(request.POST)
        form = ProviderDescriptionForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
    else:
        form = ProviderDescriptionForm(instance=provider)
    return render(request, 'providers/provider_description_form.html', {'form': form})
