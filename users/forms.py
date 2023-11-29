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
    email = forms.EmailField()
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
        email = cleaned_data.get('email')

        if user_type == 'member':
            if User.objects.filter(email=email, is_member=True).exists():
                raise ValidationError(_('A member with that email already exists.'))
        elif user_type == 'provider':
            if User.objects.filter(email=email, is_provider=True).exists():
                raise ValidationError(_('A provider with that email already exists.'))

        if user_type == 'member':
            cleaned_data['is_member'] = True
        elif user_type == 'provider':
            cleaned_data['is_provider'] = True

        return cleaned_data


class UserLoginForm(AuthenticationForm):
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'next']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'city', 'state', 'zip_code', 'bio']


class UserProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
