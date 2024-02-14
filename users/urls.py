from django.urls import path
from users.views import register, login, logout, profile, profile_image_update

urlpatterns = [
    path("register/", register, name="users-register"),
    path("login/", login, name="users-login"),
    path("logout/", logout, name="users-logout"),
    path("profile/", profile, name="users-profile"),
    path("profile/image/", profile_image_update, name="users-profile-image"),
]
