from datetime import date, datetime
from django.db import models
from django.urls import reverse


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
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    weekday = models.CharField(max_length=20, choices=WEEKDAYS, blank=True, null=True)
    age_group = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    price_in_cents = models.IntegerField(blank=True, null=True)
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
        # fix TypeError: unsupported operand type(s) for -: 'datetime.time' and 'datetime.time'
        # old code: return self.end_time - self.start_time
        timespan = datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)
        # return formatted timespan HH"h" MM"m"
        return f'{timespan.seconds // 3600}h {timespan.seconds % 3600 // 60}m'


    def get_price(self):
        # format price in dollars and cents with 0 zeros
        return f'{self.price_in_cents / 100:.2f} {self.price_currency} / {self.price_period}'
