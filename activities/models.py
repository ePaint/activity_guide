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

LOCATIONS = [
    ('Aberdeen', 'Aberdeen'),
    ('Barnhartvale', 'Barnhartvale'),
    ('Batchlor Heights', 'Batchlor Heights'),
    ('Brocklehurst', 'Brocklehurst'),
    ('Campble Creek', 'Campble Creek'),
    ('Dallas', 'Dallas'),
    ('Downtown', 'Downtown'),
    ('Harper Mountain', 'Harper Mountain'),
    ('Juniper Ridge', 'Juniper Ridge'),
    ('Kamloops', 'Kamloops'),
    ('McArthur Island', 'McArthur Island'),
    ('North Kamloops', 'North Kamloops'),
    ('Rayleigh / Heffley', 'Rayleigh / Heffley'),
    ('Sahali Lower', 'Sahali Lower'),
    ('Sahali Upper', 'Sahali Upper'),
    ('Sun Peaks', 'Sun Peaks'),
    ('TRU', 'TRU'),
    ('Valleyview', 'Valleyview'),
    ('Westsyde', 'Westsyde')
]

ACTIVITY_TYPES = [
    ('Session', 'Session'),
    ('Camp', 'Camp'),
    ('Drop-in', 'Drop-in'),
    ('Party', 'Party'),
]

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='activities', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='activities')
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, blank=True, null=True, related_name='activities')
    from_date = models.DateField()
    to_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    weekday = models.CharField(max_length=20, choices=WEEKDAYS, blank=True, null=True)
    age_start = models.IntegerField()
    age_end = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=20, choices=LOCATIONS, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_period = models.CharField(max_length=20, choices=PRICE_PERIODS)
    capacity = models.IntegerField(blank=True, null=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    is_visually_adaptive = models.BooleanField(default=False)
    is_hearing_adaptive = models.BooleanField(default=False)
    is_mobility_adaptive = models.BooleanField(default=False)
    is_cognitive_adaptive = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        ordering = ['created_at']
    
    def get_absolute_url(self):
        return reverse('activity-detail', kwargs={'slug': self.slug})
    
    def get_duration(self):
        if not self.start_time or not self.end_time:
            return None
        
        timespan = datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)
        return f'{timespan.seconds // 3600}h {timespan.seconds % 3600 // 60}m'

    def get_age_group(self):
        if not self.age_start and not self.age_end:
            return 'All ages'
        if not self.age_start:
            return f'Up to {self.age_end} years old'
        if not self.age_end:
            return f'From {self.age_start} years old'
        return f'From {self.age_start} to {self.age_end} years old'

    def get_price(self):
        if not self.price:
            return 'Free'
        
        if not self.price_period:
            return f'{self.price} CAD'
        
        return f'{self.price} CAD / {self.price_period}'
    
    def image_url(self):
        if self.image:
            return self.image.url
        return STATIC_URL + 'layout/image-alt.svg' 
    
    def get_color(self):
        if self.is_featured or self.provider.is_featured:
            return 'yellow'
        return self.category.get_color()
    
    
    def get_adaptive_fields(self):
        fields = [
            {
                'slug': 'visually-adaptive',
                'title': 'Visually adaptive',
                'description': 'Visually adaptability is a feature that allows people with visual disabilities to enjoy the activity.',
                'icon': STATIC_URL + 'layout/eye-fill.svg',
                'enabled': self.is_visually_adaptive,
            },
            {
                'slug': 'hearing-adaptive',
                'title': 'Hearing adaptive',
                'description': 'Hearing adaptability is a feature that allows people with hearing disabilities to enjoy the activity.',
                'icon': STATIC_URL + 'layout/ear-fill.svg',
                'enabled': self.is_hearing_adaptive,
            },
            {
                'slug': 'mobility-adaptive',
                'title': 'Mobility adaptive',
                'description': 'Mobility adaptability is a feature that allows people with mobility disabilities to enjoy the activity.',
                'icon': STATIC_URL + 'layout/person-wheelchair.svg',
                'enabled': self.is_mobility_adaptive,
            },
            {
                'slug': 'cognitive-adaptive',
                'title': 'Cognitive adaptive',
                'description': 'Cognitive adaptability is a feature that allows people with cognitive disabilities to enjoy the activity.',
                'icon': STATIC_URL + 'layout/lightbulb-fill.svg',
                'enabled': self.is_cognitive_adaptive,
            }
        ]
        
        return [field for field in fields if field['enabled']]
    
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
    
    def get_capacity_form(self):
        return ActivityCapacityForm(instance=self, field='capacity')
    
    def get_activity_type_form(self):
        return ActivityActivityTypeForm(instance=self, field='activity_type')
    
    def get_url_form(self):
        return ActivityUrlForm(instance=self, field='url')
    
    def get_is_visually_adaptive_form(self):
        return ActivityIsVisuallyAdaptiveForm(instance=self, field='is_visually_adaptive')

    def get_is_hearing_adaptive_form(self):
        return ActivityIsHearingAdaptiveForm(instance=self, field='is_hearing_adaptive')
    
    def get_is_mobility_adaptive_form(self):
        return ActivityIsMobilityAdaptiveForm(instance=self, field='is_mobility_adaptive')
    
    def get_is_cognitive_adaptive_form(self):
        return ActivityIsCognitiveAdaptiveForm(instance=self, field='is_cognitive_adaptive')
    
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
            self.get_price_period_form(),
            self.get_location_form(),
            self.get_capacity_form(),
            self.get_activity_type_form(),
            self.get_url_form(),
            self.get_is_visually_adaptive_form(),
            self.get_is_hearing_adaptive_form(),
            self.get_is_mobility_adaptive_form(),
            self.get_is_cognitive_adaptive_form(),
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
            'hx-post': f'/activities/{self.instance.pk}/{field}/edit/',
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
        widgets = {'location': forms.Select(attrs={'class': 'form-control'})}

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

class ActivityCapacityForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['capacity']
        widgets = {'capacity': forms.NumberInput(attrs={'class': 'form-control'})}

class ActivityActivityTypeForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['activity_type']
        widgets = {'activity_type': forms.Select(attrs={'class': 'form-control'})}
        
class ActivityUrlForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['url']
        widgets = {'url': forms.URLInput(attrs={'class': 'form-control'})}
        
class ActivityIsVisuallyAdaptiveForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['is_visually_adaptive']
        widgets = {'is_visually_adaptive': forms.CheckboxInput(attrs={'class': 'form-check-input form-control w-25 ms-auto'})}

class ActivityIsHearingAdaptiveForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['is_hearing_adaptive']
        widgets = {'is_hearing_adaptive': forms.CheckboxInput(attrs={'class': 'form-check-input form-control w-25 ms-auto'})}

class ActivityIsMobilityAdaptiveForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['is_mobility_adaptive']
        widgets = {'is_mobility_adaptive': forms.CheckboxInput(attrs={'class': 'form-check-input form-control w-25 ms-auto'})}
        
class ActivityIsCognitiveAdaptiveForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['is_cognitive_adaptive']
        widgets = {'is_cognitive_adaptive': forms.CheckboxInput(attrs={'class': 'form-check-input form-control w-25 ms-auto'})}

class ActivityIsActiveForm(ActivityBaseForm):
    class Meta:
        model = Activity
        fields = ['is_active']
        widgets = {'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input form-control w-25 ms-auto'})}


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
    'capacity': ActivityCapacityForm,
    'activity_type': ActivityActivityTypeForm,
    'url': ActivityUrlForm,
    'is_visually_adaptive': ActivityIsVisuallyAdaptiveForm,
    'is_hearing_adaptive': ActivityIsHearingAdaptiveForm,
    'is_mobility_adaptive': ActivityIsMobilityAdaptiveForm,
    'is_cognitive_adaptive': ActivityIsCognitiveAdaptiveForm,
    'is_active': ActivityIsActiveForm,
}