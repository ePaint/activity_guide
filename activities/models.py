from datetime import date, datetime
from django import forms
from django.db import models
from django.urls import reverse
from activity_guide.settings import STATIC_URL
from categories.models import Category


WEEKDAYS = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday')
]

PRICE_PERIODS = [
    ('day', 'day'),
    ('week', 'week'),
    ('month', 'month'),
    ('year', 'year')
]

CURRENCIES = [
    ('CAD', 'CAD'),
    ('USD', 'USD')
]

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='activities', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='activities')
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, blank=True, null=True, related_name='activities')
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    weekday = models.CharField(max_length=20, choices=WEEKDAYS, blank=True, null=True)
    age_start = models.IntegerField(blank=True, null=True)
    age_end = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_period = models.CharField(max_length=20, choices=PRICE_PERIODS, blank=True, null=True)
    price_currency = models.CharField(max_length=3, default='CAD', choices=CURRENCIES)
    capacity = models.IntegerField(blank=True, null=True)
    activity_type = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        ordering = ['created_at']
    
    def get_absolute_url(self):
        return reverse('activity-detail', kwargs={'slug': self.slug})
    
    def get_duration(self):
        timespan = datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)
        return f'{timespan.seconds // 3600}h {timespan.seconds % 3600 // 60}m'

    def get_age_group(self):
        return f'{self.age_start}-{self.age_end}'

    def get_price(self):
        return f'{self.price} {self.price_currency} / {self.price_period}'
    
    def image_url(self):
        if self.image:
            return self.image
        return STATIC_URL + 'layout/image-alt.svg' 
    
    def get_name_form(self):
        return ActivityNameForm(instance=self, field='name')
    
    def get_description_form(self):
        return ActivityDescriptionForm(instance=self, field='description')
    
    def get_category_form(self):
        return ActivityCategoryForm(instance=self, field='category')
    
    def get_provider_form(self):
        return ActivityProviderForm(instance=self, field='provider')
    
    def get_from_date_form(self):
        return ActivityFromDateForm(instance=self, field='from_date')
    
    def get_to_date_form(self):
        return ActivityToDateForm(instance=self, field='to_date')
    
    def get_start_time_form(self):
        return ActivityStartTimeForm(instance=self, field='start_time')
    
    def get_end_time_form(self):
        return ActivityEndTimeForm(instance=self, field='end_time')
    
    def get_weekday_form(self):
        return ActivityWeekdayForm(instance=self, field='weekday')
    
    def get_age_start_form(self):
        return ActivityAgeStartForm(instance=self, field='age_start')
    
    def get_age_end_form(self):
        return ActivityAgeEndForm(instance=self, field='age_end')
    
    def get_position_form(self):
        return ActivityPositionForm(instance=self, field='position')
    
    def get_location_form(self):
        return ActivityLocationForm(instance=self, field='location')
    
    def get_price_form(self):
        return ActivityPriceForm(instance=self, field='price')
    
    def get_price_period_form(self):
        return ActivityPricePeriodForm(instance=self, field='price_period')
    
    def get_price_currency_form(self):
        return ActivityPriceCurrencyForm(instance=self, field='price_currency')
    
    def get_capacity_form(self):
        return ActivityCapacityForm(instance=self, field='capacity')
    
    def get_activity_type_form(self):
        return ActivityActivityTypeForm(instance=self, field='activity_type')
    
    def get_is_active_form(self):
        return ActivityIsActiveForm(instance=self, field='is_active')
    
    def get_edit_forms(self):
        return [
            self.get_from_date_form(),
            self.get_to_date_form(),
            self.get_start_time_form(),
            self.get_end_time_form(),
            self.get_age_start_form(),
            self.get_age_end_form(),
            self.get_weekday_form(),
            self.get_position_form(),
            self.get_price_form(),
            self.get_price_currency_form(),
            self.get_price_period_form(),
            self.get_location_form(),
            self.get_capacity_form(),
            self.get_activity_type_form(),
            self.get_is_active_form(),
        ]
    
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ActivityBaseForm(forms.ModelForm):
    prev_value = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, field=None, **kwargs):
        super(ActivityBaseForm, self).__init__(*args, **kwargs)
        self.fields[field].widget.attrs.update({
            'id': f'{self.instance.pk}-{field}',
            'hx-post': f'/activities/{self.instance.pk}/{field}/edit',
            'hx-target': f'#activity_{self.instance.pk}-{field}',
            'hx-trigger': 'keyup delay:500ms, change delay:500ms',
            'onkeydown': 'showLoadingSpinner(this)',
            'onchange': 'showLoadingSpinner(this)',
            'hx-on::after-request': 'hideLoadingSpinner(this)',
            'hx-swap': 'outerHTML',
        })
        self.fields['prev_value'].widget.attrs.update({
            'value': getattr(self.instance, field),
        })

class ActivityNameForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class ActivityDescriptionForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['description']
        widgets = {'description': forms.Textarea(attrs={'class': 'form-control'})}

class ActivityCategoryForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['category']
        widgets = {'category': forms.Select(attrs={'class': 'form-control'})}

class ActivityCategoryForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['category']
        widgets = {'category': forms.Select(attrs={'class': 'form-control'})}

class ActivityProviderForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['provider']
        widgets = {'provider': forms.Select(attrs={'class': 'form-control'})}

class ActivityFromDateForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['from_date']
        widgets = {'from_date': DateInput(attrs={'class': 'form-control'})}

class ActivityToDateForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['to_date']
        widgets = {'to_date': DateInput(attrs={'class': 'form-control'})}
    
class ActivityStartTimeForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['start_time']
        widgets = {'start_time': TimeInput(attrs={'class': 'form-control'})}

class ActivityEndTimeForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['end_time']
        widgets = {'end_time': TimeInput(attrs={'class': 'form-control'})}

class ActivityWeekdayForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['weekday']
        widgets = {'weekday': forms.Select(attrs={'class': 'form-control'})}

class ActivityAgeStartForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['age_start']
        widgets = {'age_start': forms.NumberInput(attrs={'class': 'form-control'})}

class ActivityAgeEndForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['age_end']
        widgets = {'age_end': forms.NumberInput(attrs={'class': 'form-control'})}

class ActivityPositionForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['position']
        widgets = {'position': forms.TextInput(attrs={'class': 'form-control'})}

class ActivityLocationForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['location']
        widgets = {'location': forms.TextInput(attrs={'class': 'form-control'})}

class ActivityPriceForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['price']
        widgets = {'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.25})}

class ActivityPricePeriodForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['price_period']
        widgets = {'price_period': forms.Select(attrs={'class': 'form-control'})}

class ActivityPriceCurrencyForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['price_currency']
        widgets = {'price_currency': forms.Select(attrs={'class': 'form-control'})}

class ActivityCapacityForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['capacity']
        widgets = {'capacity': forms.NumberInput(attrs={'class': 'form-control'})}

class ActivityActivityTypeForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['activity_type']
        widgets = {'activity_type': forms.TextInput(attrs={'class': 'form-control'})}

class ActivityIsActiveForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['is_active']
        widgets = {'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})}


FORM_MAPPER = {
    'name': ActivityNameForm,
    'description': ActivityDescriptionForm,
    'category': ActivityCategoryForm,
    'provider': ActivityProviderForm,
    'from_date': ActivityFromDateForm,
    'to_date': ActivityToDateForm,
    'start_time': ActivityStartTimeForm,
    'end_time': ActivityEndTimeForm,
    'weekday': ActivityWeekdayForm,
    'age_start': ActivityAgeStartForm,
    'age_end': ActivityAgeEndForm,
    'position': ActivityPositionForm,
    'location': ActivityLocationForm,
    'price': ActivityPriceForm,
    'price_period': ActivityPricePeriodForm,
    'price_currency': ActivityPriceCurrencyForm,
    'capacity': ActivityCapacityForm,
    'activity_type': ActivityActivityTypeForm,
    'is_active': ActivityIsActiveForm,
}