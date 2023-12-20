from django.db import models
from django.urls import reverse


# Providers create offers for the users to see
class Provider(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='providers', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'
        ordering = ['created_at']
    
    def get_absolute_url(self):
        return reverse('provider-detail', kwargs={'slug': self.slug})
    
    def get_offers(self):
        return self.offer_set.all().order_by('-created_at')
    
    def get_categories(self):
        return {offer.category for offer in self.offer_set.all()}
