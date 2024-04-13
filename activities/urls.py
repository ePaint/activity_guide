from django.urls import path
from activities.views import (
    activity_detail,
    activity_edit,
    activity_field_edit,
    activity_like,
    activity_like_status,
    activity_book,
    activity_book_buttons,
    activity_book_direct,
    activity_create,
    activity_provider_edit_list,
    activity_image_update,
)

urlpatterns = [
    path("<slug:slug>/image/", activity_image_update, name="activity-image-update"),
    path("create/", activity_create, name="activity-create"),
    path("<slug:slug>/", activity_detail, name="activity-detail"),
    path("<slug:slug>/edit/", activity_edit, name="activity-edit"),
    path("<int:pk>/<str:field>/edit/", activity_field_edit, name="activity-field-edit"),
    path("<slug:slug>/like/", activity_like, name="activity-like"),
    path("<slug:slug>/like/status/", activity_like_status, name="activity-like-status"),
    path("<slug:slug>/book/", activity_book, name="activity-book"),
    path("<slug:slug>/book/buttons/", activity_book_buttons, name="activity-book-buttons"),
    path("<slug:slug>/book/direct/", activity_book_direct, name="activity-book-direct"),
    path("edit/activity/list/", activity_provider_edit_list, name="activity-provider-edit-list"),
    
]
