from django.urls import path
from categories.views import home

urlpatterns = [
    path('', home, name='categories-home'),
]
