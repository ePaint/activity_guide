from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from providers.models import Provider
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.core.files.base import ContentFile
import base64


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


class ProviderForm(forms.ModelForm):
    slug = forms.SlugField(max_length=100, required=True, label='Custom URL', help_text=_('- A unique identifier for the provider. This will be used in the URL for the provider\'s profile page.</br>- Allowed characters: a-z, 0-9, and -</br>- Example: my-provider-1'))

    class Meta:
        model = Provider
        fields = ['name', 'slug', 'description', 'image']

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if len(slug) < 3:
            raise ValidationError(_('Custom URL must be at least 3 characters long.'))

        try:
            provider = Provider.objects.get(slug=slug)
        except Provider.DoesNotExist:
            provider = None
        

        if provider and provider.id != self.instance.id:
            raise ValidationError(_('A provider with this custom URL already exists.'))
        
        #validate allowed characters: a-z (lowercase only), 0-9, and -
        print('ACA HAY UN CHAR')
        for char in slug:
            if not char.isalnum() and char != '-':
                raise ValidationError(_('Custom URL can only contain a-z, 0-9, and -'))
            if char.isupper():
                raise ValidationError(_('Custom URL can only contain lowercase letters.'))
            print(char.isupper())
        return slug


class ProviderImageForm(forms.ModelForm):
    image_data_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Provider
        fields = ['image']
    
    def save(self, commit=True):
        form_object = super().save(commit=False)
        image_data_url = self.cleaned_data.get('image_data_url')
        image = self.cleaned_data.get('image')
        if image_data_url:
            format, imgstr = image_data_url.split(';base64,')
            ext = format.split('/')[-1]
            form_object.image.save(
                f"provider_image.{ext}",
                ContentFile(base64.b64decode(imgstr)),
                save=False
            )
            
        if image:
            self.instance.image = image
        print(f'Image: {image}. Instance: {self.instance}. Commit: {commit}')
        
        if commit:
            form_object.save()
        return form_object