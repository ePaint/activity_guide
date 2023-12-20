from django.urls import path
from offers.views import offer_detail

urlpatterns = [
    path('<slug:slug>/', offer_detail, name='offer-detail')
]
