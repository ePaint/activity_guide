from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from activities.models import Activity
from providers.models import Provider
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class ProviderNameForm(forms.ModelForm):
    template_name = 'providers/provider_name_form.html'
    name = forms.CharField(max_length=100, required=True, label='')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise ValidationError(_('Name must be at least 3 characters long.'))

        try:
            provider = Provider.objects.get(name=name)
        except Provider.DoesNotExist:
            provider = None

        if provider and provider.id != self.instance.id:
            print('form:', provider.id)
            print('instance:', self.instance.id)
            raise ValidationError(_('A provider with this name already exists.'))
        
        return name
    
    class Meta:
        model = Provider
        fields = ['name']


class ProviderDescriptionForm(forms.ModelForm):
    template_name = 'providers/provider_description_form.html'
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Provider
        fields = ['description']


class DateInput(forms.DateInput):
    input_type = "date"
    

class TimeInput(forms.TimeInput):
    input_type = 'time'

        
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            "name",
            "description",
            "category",
            "from_date",
            "to_date",
            "start_time",
            "end_time",
            "weekday",
            "age_start",
            "age_end",
            "position",
            "location",
            "price",
            "price_period",
            "price_currency",
            "capacity",
            "activity_type",
            "slug",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name here..."}),
            "description": forms.Textarea(attrs={"placeholder": "Description here..."}),
            "from_date": DateInput(),
            "to_date": DateInput(),
            "start_time": TimeInput(),
            "end_time": TimeInput(),
            "weekday": forms.Select(attrs={'class': 'form-control'}),
            "age_start": forms.NumberInput(attrs={"placeholder": "Start age here..."}),
            "age_end": forms.NumberInput(attrs={"placeholder": "End age here..."}),
            "position": forms.TextInput(attrs={"placeholder": "Position here..."}),
            "location": forms.TextInput(attrs={"placeholder": "Location here..."}),
            "price": forms.NumberInput(attrs={"placeholder": "Price here..."}),
            "price_period": forms.Select(attrs={'class': 'form-control'}),
            "price_currency": forms.Select(attrs={'class': 'form-control'}),
            "capacity": forms.NumberInput(attrs={"placeholder": "Capacity here..."}),
            "activity_type": forms.Select(attrs={'class': 'form-control'}),
            "slug": forms.TextInput(attrs={"placeholder": "Slug here..."}),
        }