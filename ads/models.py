from django.db import models
AD_LOCATIONS = [
    ('H', 'Homepage Top Ads'),
    ('S', 'Search Results Top Ads'),
    ('S1', 'Search Results Sidebar #1 Ads'),
    ('S2', 'Search Results Sidebar #2 Ads'),
    ('C1', 'Categories Top-left Ads'),
    ('C2', 'Categories Top-middle Ads'),
    ('C3', 'Categories Top-right Ads'),
    ('SC', 'Specific Category Sidebar Ads'),

]


class Ad(models.Model):
    image_url = models.URLField()
    location = models.CharField(max_length=2, choices=AD_LOCATIONS, null=True, blank=True)

    def __str__(self):
        return self.image_url
    
