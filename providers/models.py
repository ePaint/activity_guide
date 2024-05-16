import uuid
from django import forms
from django.db import models
from django.urls import reverse
from activity_guide.settings import STATIC_URL


class Provider(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to='providers', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='provider', null=True, blank=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'
        ordering = ['created_at']
        
    def get_phone(self):
        return f'({self.phone[:3]}) {self.phone[3:6]}-{self.phone[6:]}' if self.phone else ''
    
    def get_absolute_url(self):
        return reverse('provider-profile', kwargs={'slug': self.slug})
    
    def get_activities(self):
        return self.activities.all().order_by('-is_active', '-updated_at')
    
    def get_active_activities(self):
        return self.activities.filter(is_active=True).order_by('-is_featured', '-provider__is_featured', '-updated_at')
    
    def get_categories(self):
        return {activity.category for activity in self.activities.all()}
    
    def get_seed(self):
        return uuid.uuid4().hex

    def image_url(self):
        if self.image:
            return self.image.url
        return STATIC_URL + 'layout/image-alt.svg'
    
    def get_name_form(self):
        return ProviderNameForm(instance=self, field='name')
    
    def get_description_form(self):
        return ProviderDescriptionForm(instance=self, field='description')
    
    def get_url_form(self):
        return ProviderUrlForm(instance=self, field='url')
    
    def get_phone_form(self):
        return ProviderPhoneForm(instance=self, field='phone')
    
    def get_email_form(self):
        return ProviderEmailForm(instance=self, field='email')

class ProviderBaseForm(forms.ModelForm):
    prev_value = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, field=None, **kwargs):
        super(ProviderBaseForm, self).__init__(*args, **kwargs)
        self.fields[field].widget.attrs.update({
            'id': f'{self.instance.pk}-{field}',
            'hx-post': f'/providers/{self.instance.pk}/{field}/edit/',
            'hx-target': f'#provider_{self.instance.id}-{field}',
            'hx-trigger': 'keyup delay:2000ms, change delay:2000ms',
            'onkeydown': 'showLoadingSpinner(this)',
            'onchange': 'showLoadingSpinner(this)',
            'hx-on::after-request': 'hideLoadingSpinner(this)',
            'hx-swap': 'outerHTML',
        })
        self.fields['prev_value'].widget.attrs.update({
            'value': getattr(self.instance, field),
        })
        
class ProviderNameForm(ProviderBaseForm):
    class Meta:
        model = Provider
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}
        
class ProviderDescriptionForm(ProviderBaseForm):
    class Meta:
        model = Provider
        fields = ['description']
        widgets = {'description': forms.Textarea(attrs={'class': 'form-control provider-description-form'})}
        
class ProviderUrlForm(ProviderBaseForm):
    class Meta:
        model = Provider
        fields = ['url']
        widgets = {'url': forms.URLInput(attrs={'class': 'form-control'})}
        
class ProviderPhoneForm(ProviderBaseForm):
    class Meta:
        model = Provider
        fields = ['phone']
        widgets = {'phone': forms.TextInput(attrs={'class': 'form-control'})}

class ProviderEmailForm(ProviderBaseForm):
    class Meta:
        model = Provider
        fields = ['email']
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control'})}
        

FORM_MAPPER = {
    'name': ProviderNameForm,
    'description': ProviderDescriptionForm,
    'url': ProviderUrlForm,
    'phone': ProviderPhoneForm,
    'email': ProviderEmailForm,
}