from django.urls import path
from activities.views import activity_detail

urlpatterns = [
    path('<slug:slug>/', activity_detail, name='activity-detail')
]
