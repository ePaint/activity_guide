from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import loader, Context

from categories.models import Category
from activities.models import Activity
from django.core.mail import EmailMultiAlternatives

from layout.forms import ContactForm


def not_found(request, exception):
    print(f'404 error')
    return render(request, 'layout/404.html')


def server_error(request):
    print(f'500 error')
    return render(request, 'layout/500.html')


def not_ready(request):
    print(f'Not ready')
    return render(request, 'layout/not_ready.html')


def base(request):
    return render(request, 'layout/base.html')


def home(request):
    categories = Category.objects.all().order_by('created_at')[:3]
    activities = Activity.objects.all().order_by('?')[:5]
    context = {
        'categories': categories,
        'activities': activities
    }
    return render(request, 'layout/home.html', context)


def navbar(request):
    return render(request, 'layout/navbar.html')


def search_results(request):
    activities = Activity.objects.all()
    context = {
        'activities': activities
    }
    return render(request, 'layout/search_results.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return render(request, 'layout/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'layout/contact.html', {'form': form})
