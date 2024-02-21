from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import resolve
from layout.decorators import login_required, provider_required
from layout.views import field_edit
from providers.forms import ProviderForm, ProviderImageForm, ProviderNameForm, ProviderDescriptionForm
from providers.models import FORM_MAPPER, Provider


def provider_profile(request, slug):
    provider = Provider.objects.get(slug=slug)
    context = {
        'provider': provider,
    }
    return render(request, 'providers/provider_profile.html', context)


@provider_required
def provider_dashboard(request):
    provider = Provider.objects.get(user=request.user)
    context = {
        'provider': provider,
    }
    return render(request, 'providers/provider_dashboard.html', context)


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
        form = ProviderDescriptionForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
    else:
        form = ProviderDescriptionForm(instance=provider)
    return render(request, 'providers/provider_description_form.html', {'form': form})


def provider_request_form(request):
    try:
        provider = Provider.objects.get(user=request.user)
    except Provider.DoesNotExist:
        provider = Provider(user=request.user)
    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES, instance=provider)
        if form.is_valid():
            provider = form.save(commit=False)
            provider.save()
            request.user.is_provider = True
            request.user.save()
            response = render(request, 'providers/provider_dashboard.html', {'provider': provider})
            response.headers['HX-Replace-Url'] = '/providers/dashboard'
            response.headers['HX-Retarget'] = '#main-content'
            response.headers['HX-Trigger'] = 'close-modal, reload-navbar'
            return response
    else:
        form = ProviderForm(instance=provider)
    context = {
        'form': form,
        'title': 'Become a Provider',
        'submit_label': 'Submit Request',
        'endpoint': request.path,
        'close_on_submit': False,
    }
    return render(request, 'layout/partials/form.html', context)


def provider_image_update(request):
    if request.method == 'POST':
        form = ProviderImageForm(request.POST, instance=request.user.provider)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)


def provider_field_edit(request, pk, field):
    return field_edit(request, Provider, 'provider', pk, field, FORM_MAPPER[field])
