from django.http import HttpResponse
from django.shortcuts import render, redirect
from layout.decorators import login_required
from layout.forms import ConfirmForm
from layout.views import field_edit
from members.models import FORM_MAPPER, FamilyMember, Member
from .forms import FamilyMemberForm


def member_profile(request):
    return render(request, 'members/member_profile.html')

@login_required
def member_dashboard(request):
    print(request.user)
    context = {
        'member': Member.objects.get(user=request.user)
    }
    return render(request, 'members/member_dashboard.html')


def family_member_list(request):
    return render(request, 'members/partials/family_member_list.html')


def add_family_member(request):
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST)
        if form.is_valid():
            family_member = form.save(commit=False)
            family_member.member = Member.objects.get(user=request.user)
            family_member.save()
            response = HttpResponse(status=204)
            response.headers['HX-Trigger'] = 'reload-family-member-list'
            return response
    else:
        form = FamilyMemberForm()
    
    context = {
        'form': form,
        'title': 'Add Family Member',
        'submit_label': 'Add',
        'endpoint': request.path,
        'close_on_submit': True,
    }
    return render(request, 'layout/partials/form.html', context)


def remove_family_member(request, pk):
    family_member = FamilyMember.objects.get(pk=pk)

    submit_label = 'Yes, delete'
    submit_color = 'red'
    confirm_label = f'Are you sure you want to delete {family_member.name}?'
    confirm_message=f'You are about to delete a family member. All information and activities booked by this person will be lost.</br></br><b class="red">This action cannot be undone.</b>'
    
    
    if request.method == "POST":
        form = ConfirmForm(request.POST, confirm_label=confirm_label, confirm_message=confirm_message)
        if form.is_valid():
            family_member.delete()
            response = HttpResponse(status=204)
            response.headers['HX-Trigger'] = 'reload-family-member-list'
            return response
    else:
        form = ConfirmForm(confirm_label=confirm_label, confirm_message=confirm_message)
    
    context = {
        'form': form,
        'title': 'Confirm Action',
        'submit_label': submit_label,
        'submit_color': submit_color,
        'endpoint': request.path,
        'close_on_submit': True,
    }
    return render(request, "layout/partials/form.html", context)


def family_member_field_edit(request, pk, field):
    return field_edit(request, FamilyMember, 'family_member', pk, field, FORM_MAPPER[field])

def family_member_search_box(request, pk):
    family_member = FamilyMember.objects.get(pk=pk)
    activities = family_member.activities.all()
    context = {
        'family_member': family_member,
        'activities': activities
    }
    return render(request, 'layout/search_box.html', context)
