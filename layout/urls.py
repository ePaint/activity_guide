from django.urls import path
from layout.views import base, home, privacy_policy, navbar, search_results, search_results_partial, contact, search_box_results

urlpatterns = [
    path('', home, name='layout-home'),
    path('privacy_policy/', privacy_policy, name='layout-privacy-policy'),
    path('navbar/', navbar, name='layout-navbar'),
    path('search_results/', search_results, name='layout-search-results'),
    path('search_results_partial/', search_results_partial, name='layout-search-results-partial'),
    path('search_box_results/', search_box_results, name='layout-search-box-results'),
    path('contact/', contact, name='layout-contact')
]
