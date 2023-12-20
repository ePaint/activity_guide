from django.db import models
from django.urls import reverse


class Offer(models.Model):
    provider = models.ForeignKey('providers.Provider', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='offers', blank=True, null=True)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('offer-detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        ordering = ['created_at']
