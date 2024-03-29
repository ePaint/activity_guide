from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import loader, Context
from django.db.models import Q

from activities.forms import ActivitySearchForm
from activity_guide.settings import PAGE_SIZE
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

def _paginate(items, page):
    page = int(page) if page else 1
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE if len(items) > start + PAGE_SIZE else len(items)
    items = items[start:end] if items else []
    return items, page + 1

def _build_search_query(form: ActivitySearchForm):
    form.is_valid()
    data = form.cleaned_data
    
    keyword = data.get('keyword')
    category = form.data.get('category')
    activity_type = data.get('activity_type')
    provider_name = data.get('provider_name')
    weekdays = data.get('weekdays')
    age = data.get('age')
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    location = data.get('location')
    position = data.get('position')
    is_visually_adaptive = data.get('is_visually_adaptive')
    is_hearing_adaptive = data.get('is_hearing_adaptive')
    is_mobility_adaptive = data.get('is_mobility_adaptive')
    is_cognitive_adaptive = data.get('is_cognitive_adaptive')
    
    query = Q()
    if keyword:
        query = query & (
            Q(name__icontains=keyword) | 
            Q(description__icontains=keyword) | 
            Q(category__name__icontains=keyword) | 
            Q(category__parent__name__icontains=keyword) | 
            Q(category__parent__parent__name__icontains=keyword))
    if category:
        query = query & (Q(category__id=category) | 
                         Q(category__parent__id=category) | 
                         Q(category__parent__parent__id=category))
    if activity_type:
        query = query & Q(activity_type__icontains=activity_type)
    if provider_name:
        query = query & Q(provider__name__icontains=provider_name)
    if weekdays:
        query = query & Q(weekday__in=weekdays)
    if age:
        query = query & Q(age_start__lte=age) & Q(age_end__gte=age)
    if from_date:
        query = query & Q(from_date__lte=from_date) & Q(to_date__gte=from_date)
    if to_date:
        query = query & Q(to_date__lte=to_date) & Q(from_date__lte=to_date)
    if start_time:
        query = query & Q(start_time__lte=start_time) & Q(end_time__gte=start_time)
    if end_time:
        query = query & Q(end_time__gte=end_time) & Q(start_time__lte=end_time)
    if location:
        query = query & Q(location__icontains=location)
    if position:
        query = query & Q(position__icontains=position)
    if is_visually_adaptive:
        query = query & Q(is_visually_adaptive=True)
    if is_hearing_adaptive:
        query = query & Q(is_hearing_adaptive=True)
    if is_mobility_adaptive:
        query = query & Q(is_mobility_adaptive=True)
    if is_cognitive_adaptive:
        query = query & Q(is_cognitive_adaptive=True)
        
    return query

def search_results(request):
    form = ActivitySearchForm(request.POST)
    query = _build_search_query(form)
    activities = Activity.objects.filter(query)
    activities, next_page = _paginate(activities, request.GET.get('page'))
    
    context = {
        'activities': activities,
        'search_form': form,
        'next_page': next_page,
        'show_provider_name': 1,
    }
    return render(request, 'layout/search_results.html', context)


def search_results_partial(request):
    form = ActivitySearchForm(request.POST)
    query = _build_search_query(form)
    activities = Activity.objects.filter(query)
    activities, next_page = _paginate(activities, request.GET.get('page'))
    
    context = {
        'items': activities,
        'model': 'activity',
        'edit': False,
        'hide_search': 1,
        'next_page': next_page,
        'show_provider_name': 1,
    }
    return render(request, 'layout/partials/search_box_results.html', context)


def search_box_results(request):
    q = request.POST.get('q')
    family_member = request.POST.get('family_member')
    member = request.POST.get('member')
    category = request.POST.get('category')
    provider = request.POST.get('provider')
    edit = request.POST.get('edit')
    stage = request.POST.get('stage')
    model = request.POST.get('model', 'activity')
    query = Q()
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
    
    items = items.order_by('-updated_at')
    items, next_page = _paginate(items, request.GET.get('page'))
    
    context = {
        'items': items,
        'model': model,
        'edit': edit,
        'next_page': next_page,
    }
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