from django.db import models
from django.urls import reverse


class Provider(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='providers', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # NO = 0
    # PENDING = 1
    # ACTIVE = 2
    # BANNED = 3
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'
        ordering = ['created_at']
    
    def get_absolute_url(self):
        return reverse('provider-detail', kwargs={'slug': self.slug})
    
    def get_activities(self):
        return self.activities.all().order_by('-created_at')
    
    def get_active_activities(self):
        return self.activities.filter(is_active=True).order_by('-created_at')
    
    def get_categories(self):
        return {activity.category for activity in self.activities.all()}
