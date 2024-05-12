from django.contrib import admin
from .models import Member, FamilyMember, Relationship


admin.site.register(Member)
admin.site.register(Relationship)
admin.site.register(FamilyMember)
