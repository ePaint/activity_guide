from django.http import HttpResponse
from django.shortcuts import render
from django.urls import resolve
from django.core.exceptions import ValidationError
from activities.forms import ActivityForm, ActivityImageForm
from activities.models import FORM_MAPPER, Activity
from layout.decorators import login_required, provider_required
from layout.forms import ConfirmForm
from layout.views import field_edit
from members.forms import FamilyMemberSelectorForm
from members.models import FamilyMember
from users.forms import UserLoginForm


def activity_detail(request, slug):
    activity = Activity.objects.get(slug=slug)
    context = {"activity": activity}
    print(activity.image.__dict__)
    return render(request, "activities/view.html", context)

@login_required
@provider_required
def activity_edit(request, slug):
    activity = Activity.objects.get(slug=slug)
    if activity.provider != request.user.provider:
        raise ValidationError("You are not authorized to edit this activity.")
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
    # messages = [
    #     {
    #         'text': f'Alternatively, you can <a target="_blank" href="{activity.provider.url}">book with the provider</a>.',
    #         'type': 'info',
    #     }
    # ]
    messages = []
    extra_buttons = [
        {
            'label': 'Continue as Guest',
            'color': 'orange',
            'onclick': f'window.open("{activity.provider.url}")',
        }
    ]
    
    if not request.user.is_authenticated:
        form = UserLoginForm()
        extra_htmls = [
            f'You don\'t have an account? <a class="btn d-inline rounded orange-hover" role="button" data-bs-target="#modal_global" hx-get="/users/register/" hx-trigger="click" hx-target="#modal_global">Register</a>',
        ]
        context = {
            'form': form,
            'messages': messages,
            'extra_htmls': extra_htmls,
            'title': 'Log in to Book Activity',
            'submit_label': 'Log In',
            'endpoint': '/users/login/',
        }
        return render(request, "layout/partials/form.html", context)
    
    if request.method == "POST":
        form = FamilyMemberSelectorForm(request.POST, instance=request.user.member, activity=activity)
        if form.is_valid():
            family_members = request.user.member.family_members.all()
            selected_family_members = form.cleaned_data["family_member"]
            hx_triggers = ['close-modal']
            for family_member in family_members:
                if family_member in selected_family_members:
                    if activity not in family_member.activities.all():
                        family_member.activities.add(activity)
                        hx_triggers.append(f"searchBoxUpdate-{family_member.pk}")
                else:
                    if activity in family_member.activities.all():
                        family_member.activities.remove(activity)
                        # hx_triggers.append(f"interactionButtonsUpdate-{activity.slug}-{family_member.pk}")
                        hx_triggers.append(f"searchBoxUpdate-{family_member.pk}")
            
            response = HttpResponse(status=204)
            response.headers['HX-Trigger'] = ", ".join(hx_triggers)
            return response
    else:
        if not request.user.member.family_members.exists():
            messages.insert(0, {
                'text': 'Create family members to save activity.',
                'type': 'warning',
            })
        form = FamilyMemberSelectorForm(instance=request.user.member, activity=activity)
    
    extra_htmls = [
        f'<a class="btn d-inline green-hover" data-bs-target="#modal_global" hx-get="/members/add_family_member/?redirect_target={request.get_full_path()}&redirect_target_slug={slug}" hx-trigger="click" hx-target="#modal_global">Create New Family Member</a>',
    ]
    
    context = {
        'form': form,
        'messages': messages,
        'extra_htmls': extra_htmls,
        'extra_buttons': extra_buttons,
        'title': 'Family Activity Organizer',
        'submit_label': 'Save Changes',
        'endpoint': request.path,
        'close_on_submit': False,
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


@provider_required
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.provider = request.user.provider
            activity.save()
            response = HttpResponse(status=204)
            response.headers['HX-Trigger'] = 'reload-activity-list, close-modal'
            return response
    else:
        copy = request.GET.get('copy')
        if copy:
            activity = Activity.objects.get(pk=copy)
            activity.slug = None
            activity.created_at = None
            activity.updated_at = None
            form = ActivityForm(instance=activity)
        else:
            form = ActivityForm()
    
    context = {
        'form': form,
        'title': 'Create Activity',
        'submit_label': 'Create',
        'endpoint': request.path,
        'close_on_submit': False,
    }
    return render(request, 'layout/partials/form.html', context)


@provider_required
def activity_provider_edit_list(request):
    context = {
        "items": request.user.provider.get_activities(),
        "edit": 1,
        "stage": "provider_dashboard",
        "model": "activity",
        "title": "Provider Activities",
    }
    return render(request, "layout/search_box.html", context)


def activity_image_update(request, slug):
    activity = Activity.objects.get(slug=slug)
    if request.method == 'POST':
        form = ActivityImageForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)
