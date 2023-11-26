from django.urls import path
from layout.views import base, home, about, contact, categories


urlpatterns = [
    path('', base, name='layout-base'),
    path('home/', home, name='layout-home'),
    path('about/', about, name='layout-about'),
    path('contact/', contact, name='layout-contact'),
    path('categories/', categories, name='layout-categories'),
]
