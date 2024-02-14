from django.http import HttpResponse
from django.shortcuts import render
from django.urls import resolve
from django.core.exceptions import ValidationError
from activities.forms import ActivityForm
from activities.models import FORM_MAPPER, Activity
from layout.decorators import login_required, provider_required
from layout.forms import ConfirmForm
from layout.views import field_edit
from members.forms import FamilyMemberSelectorForm
from members.models import FamilyMember


def activity_detail(request, slug):
    activity = Activity.objects.get(slug=slug)
    context = {"activity": activity}
    return render(request, "activities/view.html", context)


def activity_edit(request, slug):
    activity = Activity.objects.get(slug=slug)
    context = {"activity": activity}
    return render(request, "activities/edit.html", context)


def activity_field_edit(request, pk, field):
    return field_edit(request, Activity, "activity", pk, field, FORM_MAPPER[field])


def activity_like(request, slug):
    if not request.user.is_authenticated:
        view = resolve("/users/login/").func
        request.method = "GET"
        response = view(request)
        response.headers["HX-Retarget"] = ".main-content"
        response.headers["HX-Push-Url"] = "/users/login/"
        return response

    member = request.user.member
    activity = Activity.objects.get(slug=slug)

    if member.liked_activities.filter(slug=slug).exists():
        member.liked_activities.remove(activity)
    else:
        member.liked_activities.add(activity)

    return render(request, "activities/partials/like.html", {"activity": activity})


def activity_like_status(request, slug):
    activity = Activity.objects.get(slug=slug)
    return render(request, "activities/partials/like.html", {"activity": activity})


def activity_book_buttons(request, slug):
    activity = Activity.objects.get(slug=slug)
    family_member_pk = request.GET.get("family_member_pk")
    family_member = None
    if family_member_pk:
        family_member = FamilyMember.objects.get(pk=family_member_pk)
    context = {"activity": activity, "family_member": family_member}
    return render(request, "activities/partials/book_buttons.html", context)


def activity_book(request, slug):
    activity = Activity.objects.get(slug=slug)
    empty_message = None
    if request.method == "POST":
        form = FamilyMemberSelectorForm(request.POST, instance=request.user.member, activity=activity)
        if form.is_valid():
            family_members = request.user.member.family_members.all()
            selected_family_members = form.cleaned_data["family_member"]
            hx_triggers = []
            for family_member in family_members:
                if family_member in selected_family_members:
                    if activity not in family_member.activities.all():
                        family_member.activities.add(activity)
                        hx_triggers.append(f"searchBoxUpdate-{family_member.pk}")
                else:
                    if activity in family_member.activities.all():
                        family_member.activities.remove(activity)
                        hx_triggers.append(f"interactionButtonsUpdate-{activity.slug}-{family_member.pk}")
            
            response = HttpResponse(status=204)
            response.headers['HX-Trigger'] = ", ".join(hx_triggers)
            return response
    else:
        if not request.user.member.family_members.exists():
            empty_message = "You need to add a family member before you can book an activity."
        form = FamilyMemberSelectorForm(instance=request.user.member, activity=activity)
    
    context = {
        'form': form,
        'empty_message': empty_message,
        'title': 'Select Family Members to Book Activity',
        'submit_label': 'Save Changes',
        'endpoint': request.path,
        'close_on_submit': True,
    }
    return render(request, "layout/partials/form.html", context)


def activity_book_direct(request, slug):        
    activity = Activity.objects.get(slug=slug)
    family_member_pk = request.GET.get("family_member_pk")
    action = request.GET.get("action")
    family_member = FamilyMember.objects.get(pk=family_member_pk)
    
    if action == "remove":
        submit_label = 'Yes, opt-out'
        submit_color = 'red'
        confirm_label = f'Are you sure you want to opt-out?'
        confirm_message=f'You are about to make <b>{family_member.name}</b> <b class="red">opt-out</b> of <b>{activity.name}</b> by <b>{activity.provider.name}</b>. If you want to book this activity again, you will need to do so manually.'
    
    else:
        submit_label = 'Yes, book'
        submit_color = 'green'
        confirm_label = f'Are you sure you want to opt-in?'
        confirm_message=f'You are about to make <b>{family_member.name}</b> <b class="green">book</b> <b>{activity.name}</b> by <b>{activity.provider.name}</b>. If you want to opt-out of this activity again, you will need to do so manually.'
    
    
    if request.method == "POST":
        form = ConfirmForm(request.POST, confirm_label=confirm_label, confirm_message=confirm_message)
        if form.is_valid():
            if action == "add":
                family_member.activities.add(activity)
            elif action == "remove":
                family_member.activities.remove(activity)
            response = HttpResponse(status=204)
            response.headers['HX-Trigger'] = f"interactionButtonsUpdate-{activity.slug}-{family_member.pk}"
            return response
    else:
        form = ConfirmForm(confirm_label=confirm_label, confirm_message=confirm_message)
    
    context = {
        'form': form,
        'title': 'Confirm Action',
        'submit_label': submit_label,
        'submit_color': submit_color,
        'endpoint': f'{request.path}?family_member_pk={family_member_pk}&action={action}',
        'close_on_submit': True,
    }
    return render(request, "layout/partials/form.html", context)


def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.provider = request.user.provider
            activity.save()
            response = HttpResponse(status=204)
            response.headers['HX-Trigger'] = 'reload-family-member-list'
            return response
    else:
        form = ActivityForm()
    
    context = {
        'form': form,
        'title': 'Create Activity',
        'submit_label': 'Create',
        'endpoint': request.path,
        'close_on_submit': True,
    }
    return render(request, 'layout/partials/form.html', context)