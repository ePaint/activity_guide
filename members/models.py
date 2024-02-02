from django.db import models
from activities.models import Activity
import datetime

from categories.models import Category


RELATIONSHIPS = {
    "Me": "Me",
    "Spuose": "Spouse",
    "Parent": "Parent",
    "Child": "Child",
    "Sibling": "Sibling",
    "Other": "Other"
}


class FamilyMember(models.Model):    
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    relationship = models.CharField(max_length=50, choices=RELATIONSHIPS.items())
    category_interest_1 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_interest_1', blank=True, null=True)
    category_interest_2 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_interest_2', blank=True, null=True)
    category_interest_3 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_interest_3', blank=True, null=True)
    activities = models.ManyToManyField(Activity)
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='family_members')

    class Meta:
        db_table = 'family_member'
        verbose_name_plural = 'Family Members'
        verbose_name = 'Family Member'
        ordering = ['date_of_birth']

    def __str__(self):
        return self.name
        
    def get_age(self):
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)


class Member(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='member')
    liked_activities = models.ManyToManyField(Activity, related_name='liked_by', blank=True, null=True)

    class Meta:
        db_table = 'member'
        verbose_name_plural = 'Members'
        verbose_name = 'Member'

    def get_family_members(self):
        return FamilyMember.objects.filter(member=self)
    
    def get_me(self):
        return FamilyMember.objects.filter(member=self, relationship='Me').first()
    
    def get_activities(self):
        activities = []
        for family_member in self.get_family_members():
            activities.extend({
                'family_member': family_member,
                'activities': family_member.activities.all()
            })
        return activities
