from django.urls import path
from providers.views import provider_form, provider_profile, provider_edit, provider_name_update, provider_description_update

urlpatterns = [
    path('<slug:slug>/', provider_profile, name='provider-profile'),
    path('<slug:slug>/edit', provider_edit, name='provider-edit'),
    path('<slug:slug>/name_update', provider_name_update, name='provider-name-update'),
    path('<slug:slug>/description_update', provider_description_update, name='provider-description-update'),
    path('provider_form', provider_form, name='provider-form'),
]
