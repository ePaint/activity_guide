from django.urls import path
from layout.views import base, home, about, contact, categories, navbar

urlpatterns = [
    path('', home, name='layout-home'),
    path('about/', about, name='layout-about'),
    path('contact/', contact, name='layout-contact'),
    path('categories/', categories, name='layout-categories'),
    path('navbar/', navbar, name='layout-navbar'),
]
