from django.urls import path
from providers.views import provider_profile

urlpatterns = [
    path('<slug:slug>/', provider_profile, name='provider-profile')
]
