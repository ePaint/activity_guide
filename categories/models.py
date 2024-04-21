from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # image = models.ImageField(upload_to='categories', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.get_breadcrumbs()

    def get_breadcrumb_items(self):
        items = []
        if self.parent:
            items += self.parent.get_breadcrumb_items()
        items.append(self)
        return items
    
    def get_breadcrumbs(self):
        breadcrumb_items = self.get_breadcrumb_items()
        return ' > '.join([item.name for item in breadcrumb_items])

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})
    
    def get_parent(self):
        return self.parent.name if self.parent else None

    def get_children(self):
        return Category.objects.filter(parent=self).order_by('name')
    
    def get_active_children(self):
        return Category.objects.filter(parent=self, is_active=True).order_by('name')
    
    def get_activities(self):
        return self.activities.all().order_by('-is_featured', '-provider__is_featured', '-updated_at')
    
    def get_active_activities(self):
        return self.activities.filter(is_active=True, provider__is_active=True).order_by('-is_featured', '-provider__is_featured', '-updated_at')
    
    def get_unique_providers(self):
        max_providers = 10
        providers = set([activity.provider for activity in self.get_activities()])
        sorted_providers = sorted(providers, key=lambda provider: provider.name)[:max_providers]
        return {
            'items': sorted_providers,
            'show_more': len(providers) > max_providers
        }
    
    def get_active_unique_providers(self):
        max_providers = 10
        providers = set([activity.provider for activity in self.get_active_activities()])
        sorted_providers = list(providers)[:max_providers]
        return {
            'items': sorted_providers,
            'show_more': len(providers) > max_providers
        }

    def get_sorted_children(self):
        return self.get_children().order_by('name')
    
    def get_descendants(self, include_self=False):
        descendants = []
        if include_self:
            descendants.append(self)
        for child in self.get_children():
            descendants += child.get_descendants(include_self=True)
        return descendants
    
    def is_root_category(self):
        return not self.parent
    
    def get_root_category(self):
        return self if self.is_root_category() else self.parent.get_root_category()
    
    def get_activities(self):
        # get model of activities.Activity
        activity_model = self.activities.model
        return activity_model.objects.filter(category__in=self.get_descendants(include_self=True))
    
    def get_color(self):
        slug = self.get_root_category().slug
        if slug == 'sports':
            return 'orange'
        elif slug == 'art':
            return 'green'
        elif slug == 'stem':
            return 'blue'
        return 'orange'
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['created_at']
    
    