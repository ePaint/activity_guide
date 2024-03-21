from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import loader, Context
from django.db.models import Q

from activities.forms import ActivitySearchForm
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
    search_form = ActivitySearchForm()
    context = {
        'categories': categories,
        'activities': activities,
        'contact_form': contact_form,
        'search_form': search_form
    }
    return render(request, 'layout/home.html', context)


def privacy_policy(request):
    return render(request, 'layout/privacy_policy.html')


def navbar(request):
    return render(request, 'layout/navbar.html')

def _build_search_query(form: ActivitySearchForm):
    form.is_valid()
    data = form.cleaned_data
    
    name = data.get('name')
    description = data.get('description')
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    category = form.data.get('category')
    weekday = data.get('weekday')
    age_start = data.get('age_start')
    age_end = data.get('age_end')
    position = data.get('position')
    location = data.get('location')
    activity_type = data.get('activity_type')
    url = form.data.get('url')
    is_visually_adaptive = data.get('is_visually_adaptive')
    is_hearing_adaptive = data.get('is_hearing_adaptive')
    is_mobility_adaptive = data.get('is_mobility_adaptive')
    is_cognitive_adaptive = data.get('is_cognitive_adaptive')
    
    query = Q()
    if name:
        query = query & Q(name__icontains=name)
    if description:
        query = query & Q(description__icontains=description)
    if from_date:
        query = query & Q(from_date__lte=from_date) & Q(to_date__gte=from_date)
    if to_date:
        query = query & Q(to_date__lte=to_date) & Q(from_date__lte=to_date)
    if start_time:
        query = query & Q(start_time__lte=start_time) & Q(end_time__gte=start_time)
    if end_time:
        query = query & Q(end_time__gte=end_time) & Q(start_time__lte=end_time)
    if category:
        query = query & (Q(category__id=category) | Q(category__parent__id=category) | Q(category__parent__parent__id=category))
    if weekday:
        query = query & Q(weekday=weekday)
    if age_start:
        query = query & Q(age_start__lte=age_start) & Q(age_end__gte=age_start)
    if age_end:
        query = query & Q(age_end__gte=age_end) & Q(age_start__lte=age_end)
    if position:
        query = query & Q(position__icontains=position)
    if location:
        query = query & Q(location__icontains=location)
    if activity_type:
        query = query & Q(activity_type__icontains=activity_type)
    if url:
        query = query & Q(url__icontains=url)
    if is_visually_adaptive:
        query = query & Q(is_visually_adaptive=is_visually_adaptive)
    if is_hearing_adaptive:
        query = query & Q(is_hearing_adaptive=is_hearing_adaptive)
    if is_mobility_adaptive:
        query = query & Q(is_mobility_adaptive=is_mobility_adaptive)
    if is_cognitive_adaptive:
        query = query & Q(is_cognitive_adaptive=is_cognitive_adaptive)
        
    return query

def search_results(request):
    form = ActivitySearchForm(request.POST)
    query = _build_search_query(form)
    activities = Activity.objects.filter(query)    
    
    context = {
        'activities': activities,
        'search_form': form
    }
    return render(request, 'layout/search_results.html', context)


def search_results_partial(request):
    form = ActivitySearchForm(request.POST)
    query = _build_search_query(form)
    activities = Activity.objects.filter(query)
    print(query)
    context = {
        'items': activities,
        'model': 'activity',
        'edit': False,
        'hide_search': 1
    }
    return render(request, 'layout/partials/search_box_results.html', context)


def search_box_results(request):
    q = request.GET.get('q')
    family_member = request.GET.get('family_member')
    member = request.GET.get('member')
    category = request.GET.get('category')
    provider = request.GET.get('provider')
    edit = request.GET.get('edit')
    stage = request.GET.get('stage')
    model = request.GET.get('model', 'activity')
    query = Q()
    print('MODEL:', model)
    if model == 'activity':
        if q:
            query = query & Q(name__icontains=q) | (Q(category__name__icontains=q) | Q(category__parent__name__icontains=q))
        if member and stage == 'member_dashboard':
            query = query & Q(liked_by__id=member)
        if provider:
            query = query & Q(provider__id=provider)
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
        'model': model,
        'edit': edit,
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