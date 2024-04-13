from django.urls import path
from providers.views import (
    provider_field_edit,
    provider_request_form,
    provider_profile,
    provider_dashboard,
    provider_name_update,
    provider_description_update,
    provider_image_update,
)

urlpatterns = [
    path("<slug:slug>/", provider_profile, name="provider-profile"),
    path("dashboard/", provider_dashboard, name="provider-dashboard"),
    path("<slug:slug>/name_update/", provider_name_update, name="provider-name-update"),
    path("<slug:slug>/description_update/", provider_description_update, name="provider-description-update"),
    path("provider_request_form/", provider_request_form, name="provider-request-form"),
    path("image/update/", provider_image_update, name="provider-image-update"),
    path("<int:pk>/<str:field>/edit/", provider_field_edit, name="provider-field-edit"),
]
