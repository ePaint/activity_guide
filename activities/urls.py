from django.urls import path
from activities.views import activity_detail, activity_edit, activity_field_edit, activity_like

urlpatterns = [
    path('<slug:slug>/', activity_detail, name='activity-detail'),
    path('<slug:slug>/edit', activity_edit, name='activity-edit'),
    path('<int:pk>/<str:field>/edit', activity_field_edit, name='activity-field-edit'),
    path('<slug:slug>/like', activity_like, name='activity-like'),
]
