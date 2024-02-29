from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django import forms
from django.core.exceptions import ValidationError
from .models import User, UserProfile
from django.core.files.images import get_image_dimensions
from django.core.files.base import ContentFile
import base64

user_type_choices = (
    ('member', 'Member'),
    ('provider', 'Provider'),
)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'city', 'state', 'zip_code', 'bio']
        labels = {
            'zip_code': _('Postal Code')
        }
        
    
class UserProfileImageForm(forms.ModelForm):
    image_data_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = UserProfile
        fields = ['image']
    
    def save(self, commit=True):
        form_object = super().save(commit=False)
        image_data_url = self.cleaned_data.get('image_data_url')
        image = self.cleaned_data.get('image')
        if image_data_url:
            format, imgstr = image_data_url.split(';base64,')
            ext = format.split('/')[-1]
            form_object.image.save(
                f"profile_image.{ext}",
                ContentFile(base64.b64decode(imgstr)),
                save=False
            )
            
        if image:
            self.instance.image = image
        print(f'Image: {image}. Instance: {self.instance}. Commit: {commit}')
        
        if commit:
            form_object.save()
        return form_object
