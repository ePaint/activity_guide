from django.urls import path
from members.views import member_profile, member_dashboard

urlpatterns = [
    # path('sample/', member_profile, name='member-profile'),
    path('sample/dashboard', member_dashboard, name='member-dashboard'),
]
