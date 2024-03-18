from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import loader, Context
from django.db.models import Q

from categories.models import Category
from activities.models import Activity
from django.core.mail import EmailMultiAlternatives

from layout.forms import ContactForm

from django.shortcuts import render

from providers.models import Provider


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
    contact_form = ContactForm()
    context = {
        'categories': categories,
        'activities': activities,
        'contact_form': contact_form
    }
    return render(request, 'layout/home.html', context)


def privacy_policy(request):
    return render(request, 'layout/privacy_policy.html')


def navbar(request):
    return render(request, 'layout/navbar.html')


def search_results(request):
    context = {
        'activities': Activity.objects.all()
    }
    return render(request, 'layout/search_results.html', context)


def search_box_results(request):
    q = request.GET.get('q')
    family_member = request.GET.get('family_member')
    member = request.GET.get('member')
    category = request.GET.get('category')
    stage = request.GET.get('stage')
    model = request.GET.get('model', 'activity')
    query = Q()
    if model == 'activity':
        if q:
            query = query & Q(name__icontains=q) | (Q(category__name__icontains=q) | Q(category__parent__name__icontains=q))
        if member and stage == 'member_dashboard':
            query = query & Q(liked_by__id=member)
        if family_member:
            query = query & Q(family_members__id=family_member)
        items = Activity.objects.filter(query).distinct()
    elif model == 'provider':
        if q:
            query = query & Q(name__icontains=q)
        if category:
            query = query & (Q(activities__category__slug=category) | Q(activities__category__parent__slug=category))
        items = Provider.objects.filter(query).distinct()
    context = {
        'items': items,
        'model': model
    }
    print(query, "sarasaaaaaaaaaa")
    return render(request, 'layout/partials/search_box_results.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return render(request, 'layout/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'layout/contact_form.html', {'form': form})

def field_edit(request, model, model_name, pk, field, form_class):
    if request.method == 'POST':
        item = model.objects.get(pk=pk)
        form = form_class(request.POST, instance=item, field=field)
        if form.is_valid():
            form.save()
        else:
            print(form.errors.as_data())
            params = request.POST.copy()
            params[field] = request.POST.get('prev_value')
            form = form_class(params, instance=item, field=field)
        context = {
            'model': model_name,
            'item': item,
            'form': form,
        }
        return render(request, 'layout/partials/field_edit.html', context)

