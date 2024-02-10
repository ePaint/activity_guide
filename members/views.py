from django.http import HttpResponse
from django.shortcuts import render, redirect
from layout.views import field_edit
from members.models import FORM_MAPPER, FamilyMember, Member
from .forms import FamilyMemberForm
from django.contrib.auth.decorators import login_required


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
            return redirect('family-member-list')
        response = render(request, 'members/partials/add_family_member.html', {'form': form})
        response['HX-Retarget'] = "#family_member_form_container"
        return response
    else:
        form = FamilyMemberForm()
    return render(request, 'members/partials/add_family_member.html', {'form': form})


def remove_family_member(request, pk):
    family_member = FamilyMember.objects.get(pk=pk)
    family_member.delete()
    return HttpResponse('')


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
