from django.urls import path
from users.views import register, login, logout, profile

urlpatterns = [
    path('register/', register, name='users-register'),
    path('login/', login, name='users-login'),
    path('logout/', logout, name='users-logout'),
    path('profile/', profile, name='users-profile'),
]
