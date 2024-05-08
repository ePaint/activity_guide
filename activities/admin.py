from django.contrib import admin
from .models import PricePeriod, ActivityType, Location, Activity

admin.site.register(PricePeriod)
admin.site.register(ActivityType)

admin.site.register(Location)
admin.site.register(Activity)
