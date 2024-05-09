from django.db import models

from activity_guide.settings import STATIC_URL

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
        'desktop': {
            'width': 880,
            'height': 160,
        },
        'mobile': {
            'width': 768,
            'height': 236,
        },
    },
    'S': {
        'desktop': {
            'width': 1067.2,
            'height': 112,
        },
        'mobile': {
            'width': 768,
            'height': 236,
        },
    },
    'S1': {
        'desktop': {
            'width': 196,
            'height': 400,
        },
        'mobile': {
            'width': 306,
            'height': 112,
        },
    },
    'S2': {
        'desktop': {
            'width': 196,
            'height': 400,
        },
        'mobile': {
            'width': 306,
            'height': 112,
        },
    },
    'C1': {
        'desktop': {
            'width': 306,
            'height': 112,
        },
        'mobile': {
            'width': 306,
            'height': 112,
        },
    },
    'C2': {
        'desktop': {
            'width': 636,
            'height': 112,
        },
        'mobile': {
            'width': 768,
            'height': 236,
        },
    },
    'C3': {
        'desktop': {
            'width': 306,
            'height': 112,
        },
        'mobile': {
            'width': 306,
            'height': 112,
        },
    },
    'ARTS': {
        'desktop': {
            'width': 220,
            'height': 1171.3,
        },
        'mobile': {
            'width': 306,
            'height': 112,
        },
    },
    'SPORTS': {
        'desktop': {
            'width': 220,
            'height': 1171.3,
        },
        'mobile': {
            'width': 765,
            'height': 280,
        },
    },
    'STEM': {
        'desktop': {
            'width': 220,
            'height': 1171.3,
        },
        'mobile': {
            'width': 689,
            'height': 252,
        },
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
    image_desktop = models.ImageField(upload_to='ads/', null=True, blank=True)
    image_mobile = models.ImageField(upload_to='ads/', null=True, blank=True)
    location = models.ForeignKey(AdLocation, on_delete=models.SET_NULL, related_name='ads', null=True, blank=True)
    click_action = models.ForeignKey(AdClickAction, on_delete=models.SET_NULL, related_name='ads', null=True, blank=True)
    click_action_target = models.CharField(max_length=255, null=True, blank=True)

    def image_desktop_url(self):
        if self.image_desktop:
            return self.image_desktop.url
        return STATIC_URL + 'layout/image-alt.svg'
    
    def image_mobile_url(self):
        if self.image_mobile:
            return self.image_mobile.url
        if self.image_desktop:
            return self.image_desktop.url
        return STATIC_URL + 'layout/image-alt.svg'
    
    def __str__(self):
        return self.image_desktop_url()
    

def get_ads_by_location(location):
    return {
        'items': Ad.objects.filter(
            location__location=location,
            image_desktop__isnull=False,
            click_action__isnull=False,
            click_action_target__isnull=False
        ),
        'dimensions': AD_SIZES[location],
    }
