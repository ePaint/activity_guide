import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import resolve
from layout.decorators import login_required, provider_required
from layout.views import _paginate, field_edit, not_found
from providers.forms import ProviderForm, ProviderImageForm, ProviderNameForm, ProviderDescriptionForm
from providers.models import FORM_MAPPER, Provider
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context


def provider_profile(request, slug):
    try:
        provider = Provider.objects.get(slug=slug)
    except Provider.DoesNotExist as e:
        return not_found(request, e)
    activities, next_page = _paginate(provider.get_active_activities(), request.GET.get('page'))
    
    context = {
        'provider': provider,
        'activities': activities,
        'next_page': next_page,
    }
    return render(request, 'providers/provider_profile.html', context)


@login_required
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
            provider.is_active = False
            provider.save()
            request.user.is_provider = True
            request.user.save()
            base_url = request.build_absolute_uri('/')[:-1]
            send_provider_email(provider, base_url)
            response = render(request, 'providers/provider_dashboard.html', {'provider': provider})
            response.headers['HX-Replace-Url'] = '/providers/dashboard/'
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

    
def send_provider_email(provider: Provider, base_url: str):
    if not settings.CONTACT_ENABLED:
        print('Contact form is disabled.')
        return

    template = loader.get_template('providers/provider_request_email.html')
    html = template.render(context={
        'provider': provider,
        'admin_url': f'{base_url}/admin/providers/provider/{provider.id}/change/'
    })
    
    print(html)

    email = EmailMultiAlternatives(subject='New Provider Registered',
                                    to=[os.getenv('CONTACT_TO_EMAIL')],
                                    from_email=os.getenv('CONTACT_FROM_EMAIL'))
    email.attach_alternative(html, 'text/html')
    email.send()
    print('Email successfully sent to admin.')