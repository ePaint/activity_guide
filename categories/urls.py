from django.urls import path
from categories.views import home, detail

urlpatterns = [
    path('', home, name='category-home'),
    path('<slug:slug>/', detail, name='category-detail')
]
