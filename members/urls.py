from django.urls import path
from members.views import (
    family_member_list,
    member_dashboard,
    add_family_member,
    family_member_field_edit,
)

urlpatterns = [
    # path('sample/', member_profile, name='member-profile'),
    path('sample/dashboard', member_dashboard, name='member-dashboard'),
    path('family_member_list/', family_member_list, name='family-member-list'),
    path('add_family_member/', add_family_member, name='add-family-member'),
    path('<int:pk>/<str:field>/edit', family_member_field_edit, name='family-member-field-edit'),
]
