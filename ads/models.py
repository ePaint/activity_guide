from django.db import models

AD_LOCATIONS = {
    'H': 'Homepage Top Ads',
    'S': 'Search Results Top Ads',
    'S1': 'Search Results Sidebar #1 Ads',
    'S2': 'Search Results Sidebar #2 Ads',
    'C1': 'Categories Top-left Ads',
    'C2': 'Categories Top-middle Ads',
    'C3': 'Categories Top-right Ads',
    'ARTS': 'Arts Category Sidebar Ads',
    'SPORTS': 'Sports Category Sidebar Ads',
    'STEM': 'STEM Category Sidebar Ads',
}

AD_SIZES = {
    'H': {
        'width': 880,
        'height': 160,
    },
    'S': {
        'width': 1067.2,
        'height': 112,
    },
    'S1': {
        'width': 196,
        'height': 400,
    },
    'S2': {
        'width': 196,
        'height': 400,
    },
    'C1': {
        'width': 306,
        'height': 112,
    },
    'C2': {
        'width': 636,
        'height': 112,
    },
    'C3': {
        'width': 306,
        'height': 112,
    },
    'ARTS': {
        'width': 220,
        'height': 1171.3,
    },
    'SPORTS': {
        'width': 220,
        'height': 1171.3,
    },
    'STEM': {
        'width': 220,
        'height': 1171.3,
    },
}

class AdLocation(models.Model):
    location = models.CharField(max_length=10, choices=AD_LOCATIONS.items())

    def __str__(self):
        return self.location


AD_CLICK_ACTIONS = {
    'Open URL': 'Open URL',
    'Send Email': 'Send Email',
}

class AdClickAction(models.Model):
    action = models.CharField(max_length=10, choices=AD_CLICK_ACTIONS.items())

    def __str__(self):
        return self.action


class Ad(models.Model):
    image_url = models.URLField()
    location = models.ForeignKey(AdLocation, on_delete=models.CASCADE, related_name='ads')
    click_action = models.ForeignKey(AdClickAction, on_delete=models.CASCADE, related_name='ads', null=True, blank=True)
    click_action_target = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.image_url
    

def get_ads_by_location(location):
    return Ad.objects.filter(
        location__location=location,
        image_url__isnull=False,
        click_action__isnull=False,
        click_action_target__isnull=False
    )
