from django.urls import path
from layout.views import base, home, navbar, search_results, contact

urlpatterns = [
    path('', home, name='layout-home'),
    path('navbar/', navbar, name='layout-navbar'),
    path('search_results/', search_results, name='layout-search-results'),
    path('contact/', contact, name='layout-contact')
]
