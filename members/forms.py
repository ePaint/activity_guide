from django.utils.translation import gettext_lazy as _
from django import forms
from members.models import FamilyMember


class DateInput(forms.DateInput):
    input_type = "date"


class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = [
            "name",
            "date_of_birth",
            "relationship",
            "category_interest_1",
            "category_interest_2",
            "category_interest_3",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name here..."}),
            "date_of_birth": DateInput(),
            "relationship": forms.Select(attrs={"placeholder": "Relationship..."}),
        }
        exclude = ["member"]


class FamilyMemberSelectorForm(forms.ModelForm):
    family_member = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        label=_("Family Members"),
        required=False,
        help_text=_("Select family members to participate in this activity."),
    )

    class Meta:
        model = FamilyMember
        fields = ["family_member"]
        widgets = {"family_member": forms.Select(attrs={"class": "form-control"})}

    def __init__(self, *args, activity=None, **kwargs):
        super(FamilyMemberSelectorForm, self).__init__(*args, **kwargs)
        self.fields["family_member"].queryset = self.instance.family_members.all()
        # set initial values for CheckboxSelectMultiple
        # include the activity in the initial values if it exists
        filtered_activities = FamilyMember.objects.filter(activities=activity)
        print(filtered_activities)
        self.fields["family_member"].initial = filtered_activities
