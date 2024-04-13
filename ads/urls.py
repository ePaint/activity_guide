from django.urls import path
from ads.views import home, save

urlpatterns = [
    path("", home, name="ads-home"),
    path("save/<str:location>/", save, name="ads-save")
]