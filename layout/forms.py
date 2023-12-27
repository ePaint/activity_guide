from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Your name', widget=forms.TextInput(attrs={'placeholder': 'John Doe'}))
    email = forms.EmailField(required=True, label='Your email', widget=forms.TextInput(attrs={'placeholder': 'john.doe@gmail.com'}))
    # phone = forms.CharField(max_length=20, required=False, label='Your phone', widget=forms.TextInput(attrs={'placeholder': '555-555-5555'}))
    phone = PhoneNumberField(required=False, label='Your phone')
    message = forms.CharField(widget=forms.Textarea, required=True, label='Your message')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise ValidationError(_('Name must be at least 3 characters long.'))
        return name

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise ValidationError(_('Message must be at least 10 characters long.'))
        return message

    def send_email(self):
        if not settings.CONTACT_ENABLED:
            print('Contact form is disabled.')
            return
        print('Contact form is enabled. Sending email...')
        print(self.cleaned_data)
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        message = self.cleaned_data['message']

        template = loader.get_template('layout/contact_email.html')
        html = template.render(context={
            'name': name,
            'email': email,
            'phone': phone,
            'message': message,
        })

        email = EmailMultiAlternatives(subject='Customer Inquiry',
                                       to=['nsuepaint@gmail.com'],
                                       from_email='jonathanselman24@gmail.com',
                                       reply_to=[email])
        email.attach_alternative(html, 'text/html')
        email.send()
