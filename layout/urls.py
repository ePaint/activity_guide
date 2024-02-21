from django.urls import path
from layout.views import base, home, privacy_policy, navbar, search_results, contact

urlpatterns = [
    path('', home, name='layout-home'),
    path('privacy_policy/', privacy_policy, name='layout-privacy-policy'),
    path('navbar/', navbar, name='layout-navbar'),
    path('search_results/', search_results, name='layout-search-results'),
    path('contact/', contact, name='layout-contact')
]
