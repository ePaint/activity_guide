from django.utils.translation import gettext_lazy as _
from django import forms
from members.models import FamilyMember


class DateInput(forms.DateInput):
    input_type = 'date'


class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['name', 'date_of_birth', 'relationship', 'category_interest_1', 'category_interest_2', 'category_interest_3']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name here...'}),
            'date_of_birth': DateInput(),
            'relationship': forms.Select(attrs={'placeholder': 'Relationship...'}),
        }
        exclude = ['member']
        