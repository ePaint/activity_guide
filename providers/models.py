from django.db import models
from django.urls import reverse


class Provider(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='providers', blank=True, null=True)
    is_active = models.BooleanField(default=True)
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
        return self.activity_set.all().order_by('-created_at')
    
    def get_categories(self):
        return {activity.category for activity in self.activity_set.all()}
