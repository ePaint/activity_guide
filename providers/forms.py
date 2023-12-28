from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from providers.models import Provider
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class ProviderNameForm(forms.ModelForm):
    template_name = 'providers/provider_description_form.html'
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