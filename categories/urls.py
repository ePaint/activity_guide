from django.urls import path
from categories.views import home, detail

urlpatterns = [
    path('', home, name='categories-home'),
    path('<slug:slug>/', detail, name='categories-detail')
]
