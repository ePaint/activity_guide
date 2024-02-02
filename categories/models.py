from django.db import models
from django.urls import reverse
from activities.models import Activity


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.get_breadcrumbs()

    
    def get_breadcrumbs(self):
        breadcrumbs = self.name
        if self.parent:
            breadcrumbs = f'{self.parent.get_breadcrumbs()} - {breadcrumbs}'
        return breadcrumbs
    

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})
    
    def get_parent(self):
        return self.parent.name if self.parent else None
    
    def get_children(self):
        return Category.objects.filter(parent=self)
    
    def is_root_category(self):
        return not self.parent
    
    def get_root_category(self):
        return self if self.is_root_category() else self.parent.get_root_category()
    
    def get_activities(self):
        activities = []
        if self.is_root_category():
            for child in self.get_children():
                activities += child.get_activities()
        else:
            activities = Activity.objects.filter(category=self)
        return activities
    
    def get_color(self):
        slug = self.get_root_category().slug
        if slug == 'sports':
            return 'red'
        elif slug == 'art':
            return 'green'
        elif slug == 'stem':
            return 'blue'
        return 'orange'
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['created_at']
    
    