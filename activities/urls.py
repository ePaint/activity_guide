from django.urls import path
from activities.views import activity_detail, activity_edit

urlpatterns = [
    path('<slug:slug>/', activity_detail, name='activity-detail'),
    path('<slug:slug>/edit', activity_edit, name='activity-edit'),
]
