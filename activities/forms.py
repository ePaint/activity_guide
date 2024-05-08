from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from activities.models import WEEKDAYS, Activity
from providers.models import Provider
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.core.files.base import ContentFile
import base64


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
    slug = forms.SlugField(max_length=100, required=True, label='Custom URL', help_text=_('- A unique identifier for the activity. This will be used in the URL for the activity page.</br>- Allowed characters: a-z, 0-9, and -</br>- Example: my-activity-1'))

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
            "capacity",
            "activity_type",
            "is_visually_adaptive",
            "is_hearing_adaptive",
            "is_mobility_adaptive",
            "is_cognitive_adaptive",
            "slug",
            "url",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Activity Title"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
            "from_date": DateInput(attrs={"required": "required"}),
            "to_date": DateInput(attrs={"required": "required"}),
            "start_time": TimeInput(attrs={"required": "required"}),
            "end_time": TimeInput(attrs={"required": "required"}),
            "weekday": forms.Select(attrs={'class': 'form-control'}),
            "age_start": forms.NumberInput(attrs={"placeholder": "Start age in years", "required": "required"}),
            "age_end": forms.NumberInput(attrs={"placeholder": "End age in years"}),
            "position": forms.TextInput(attrs={"placeholder": "e. g. Forward, Goalie"}),
            "location": forms.Select(attrs={'class': 'form-control'}),
            "price": forms.NumberInput(attrs={"placeholder": "Price here", "required": "required"}),
            "price_period": forms.Select(attrs={'class': 'form-control', "required": "required"}),
            "capacity": forms.NumberInput(attrs={"placeholder": "How many spots are available "}),
            "activity_type": forms.Select(attrs={'class': 'form-control', "required": "required"}),
            "is_visually_adaptive": forms.CheckboxInput(),
            "is_hearing_adaptive": forms.CheckboxInput(),
            "is_mobility_adaptive": forms.CheckboxInput(),
            "is_cognitive_adaptive": forms.CheckboxInput(),
            "slug": forms.TextInput(attrs={"placeholder": "Slug here...", "required": "required"}),
            "url": forms.URLInput(attrs={"placeholder": "Paste your sign up site URL here", "required": "required"}),
        }
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if len(slug) < 3:
            raise ValidationError(_('Custom URL must be at least 3 characters long.'))

        try:
            activity = Activity.objects.get(slug=slug)
        except Activity.DoesNotExist:
            activity = None
        

        if activity and activity.id != self.instance.id:
            raise ValidationError(_('An activity with this custom URL already exists.'))
        
        for char in slug:
            if not char.isalnum() and char != '-':
                raise ValidationError(_('Custom URL can only contain a-z, 0-9, and -'))
            if char.isupper():
                raise ValidationError(_('Custom URL can only contain lowercase letters.'))
        return slug
        
        
class ActivityImageForm(forms.ModelForm):
    image_data_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Activity
        fields = ['image']
    
    def save(self, commit=True):
        form_object = super().save(commit=False)
        image_data_url = self.cleaned_data.get('image_data_url')
        image = self.cleaned_data.get('image')
        if image_data_url:
            format, imgstr = image_data_url.split(';base64,')
            ext = format.split('/')[-1]
            form_object.image.save(
                f"activity_image.{ext}",
                ContentFile(base64.b64decode(imgstr)),
                save=False
            )
            
        if image:
            self.instance.image = image
        print(f'Image: {image}. Instance: {self.instance}. Commit: {commit}')
        
        if commit:
            form_object.save()
        return form_object    

class ActivitySearchForm(forms.ModelForm):
    keyword = forms.CharField(max_length=100, required=False, label='Keyword', widget=forms.TextInput())
    age = forms.IntegerField(required=False, label='Age', widget=forms.NumberInput(), min_value=3, max_value=100)
    # weekdays = forms.MultipleChoiceField(choices=WEEKDAYS, required=False, label='Weekday', widget=forms.SelectMultiple())
    provider_name = forms.CharField(max_length=100, required=False, label='Provider', widget=forms.TextInput())
    
    class Meta:
        model = Activity
        fields = [
            "keyword",
            "category",
            "activity_type",
            "provider_name",
            "weekday",
            "age",
            "from_date",
            "to_date",
            "start_time",
            "end_time",
            "location",
            "position",
            "is_visually_adaptive",
            "is_hearing_adaptive",
            "is_mobility_adaptive",
            "is_cognitive_adaptive",
        ]
        widgets = {
            "keyword": forms.TextInput(),
            "category": forms.Select(),
            "activity_type": forms.Select(attrs={'class': 'form-control'}),
            "provider_name": forms.TextInput(),
            "weekday": forms.Select(attrs={'class': 'form-control'}),
            "age": forms.NumberInput(),
            "from_date": DateInput(),
            "to_date": DateInput(),
            "start_time": TimeInput(),
            "end_time": TimeInput(),
            "location": forms.Select(attrs={'class': 'form-control'}),
            "position": forms.TextInput(),
            "is_visually_adaptive": forms.CheckboxInput(),
            "is_hearing_adaptive": forms.CheckboxInput(),
            "is_mobility_adaptive": forms.CheckboxInput(),
            "is_cognitive_adaptive": forms.CheckboxInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        # Make categories appear alphabetically
        self.fields['category'].choices = sorted(self.fields['category'].choices, key=lambda x: x[1])
        self.fields['activity_type'].choices = sorted(self.fields['activity_type'].choices, key=lambda x: x[1])
