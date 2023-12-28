from django.urls import path
from providers.views import provider_profile, provider_dashboard, provider_name_update, provider_description_update

urlpatterns = [
    path('<slug:slug>/', provider_profile, name='provider-profile'),
    path('<slug:slug>/dashboard', provider_dashboard, name='provider-dashboard'),
    path('<slug:slug>/name_update', provider_name_update, name='provider-name-update'),
    path('<slug:slug>/description_update', provider_description_update, name='provider-description-update'),
]
