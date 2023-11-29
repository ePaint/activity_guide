from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from .models import User, UserProfile

user_type_choices = (
    ('member', 'Member'),
    ('provider', 'Provider'),
)


class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=user_type_choices,
                                  required=True,
                                  label=_('Select Account Type'),
                                  initial='member',
                                  widget=forms.RadioSelect())

    class Meta:
        model = User
        fields = ['user_type', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        cleaned_data[f'is_{user_type}'] = True
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'next']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'city', 'state', 'zip_code', 'bio']


class UserProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
