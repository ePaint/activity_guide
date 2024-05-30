from django.urls import path
from users.views import (
    UserPasswordResetView,
    register,
    login,
    logout,
    profile,
    profile_image_update,
    password_reset_done,
    UserPasswordResetConfirm,
    password_reset_complete,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", register, name="users-register"),
    path("login/", login, name="users-login"),
    path("logout/", logout, name="users-logout"),
    path("profile/", profile, name="users-profile"),
    path("profile/image/", profile_image_update, name="users-profile-image"),
    path("password-reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("password-reset-done/", password_reset_done, name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",
         UserPasswordResetConfirm.as_view(),
         name="password_reset_confirm"),
    path("password-reset-complete/", password_reset_complete, name='password_reset_complete')
]
