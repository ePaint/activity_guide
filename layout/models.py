from django.db import models


class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    show_on_home = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def __str__(self):
        return f'{self.title} ({"Shown" if self.show_on_home else "Hidden"})'
