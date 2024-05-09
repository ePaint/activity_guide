import uuid
from django import forms
from django.db import models
from activities.models import Activity
import datetime
from categories.models import Category


class Relationship(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FamilyMember(models.Model):    
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    relationship = models.ForeignKey(Relationship, on_delete=models.SET_NULL, blank=True, null=True, related_name='family_members')
    category_interest_1 = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category_interest_1', blank=True, null=True)
    category_interest_2 = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category_interest_2', blank=True, null=True)
    category_interest_3 = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='category_interest_3', blank=True, null=True)
    activities = models.ManyToManyField(Activity, related_name='family_members', blank=True, null=True)
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='family_members')

    class Meta:
        db_table = 'family_member'
        verbose_name_plural = 'Family Members'
        verbose_name = 'Family Member'
        ordering = ['date_of_birth']

    def __str__(self):
        return f'{self.name} ({self.relationship}) ({self.get_age_label()})'
        
    def get_age(self):
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)
    
    def get_age_label(self):
        return f'{self.get_age()} years old'
    
    def get_relationship_to_member(self):
        if self.relationship == 'Me':
            return 'Themselves'
        return self.relationship

    def get_name_form(self):
        return FamilyMemberNameForm(instance=self, field='name')
    
    def get_date_of_birth_form(self):
        return FamilyMemberDateOfBirthForm(instance=self, field='date_of_birth')
    
    def get_relationship_form(self):
        return FamilyMemberRelationshipForm(instance=self, field='relationship')
    
    def get_category_interest_1_form(self):
        return FamilyMemberCategoryInterest1Form(instance=self, field='category_interest_1')
    
    def get_category_interest_2_form(self):
        return FamilyMemberCategoryInterest2Form(instance=self, field='category_interest_2')
    
    def get_category_interest_3_form(self):
        return FamilyMemberCategoryInterest3Form(instance=self, field='category_interest_3')
    
    def get_edit_forms(self):
        return [
            self.get_name_form(),
            self.get_date_of_birth_form(),
            self.get_relationship_form(),
            self.get_category_interest_1_form(),
            self.get_category_interest_2_form(),
            self.get_category_interest_3_form(),
        ]

class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='member')
    liked_activities = models.ManyToManyField(Activity, related_name='liked_by', blank=True, null=True)

    class Meta:
        db_table = 'member'
        verbose_name_plural = 'Members'
        verbose_name = 'Member'
        
    def __str__(self):
        return str(self.user)

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

class DateInput(forms.DateInput):
    input_type = 'date'

class FamilyMemberBaseForm(forms.ModelForm):
    member = forms.UUIDField(widget=forms.HiddenInput())
    prev_value = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, field=None, **kwargs):
        super(FamilyMemberBaseForm, self).__init__(*args, **kwargs)
        self.fields[field].widget.attrs.update({
            'id': f'{self.instance.pk}-{field}',
            'hx-post': f'/members/{self.instance.pk}/{field}/edit/',
            'hx-target': f'#family_member_{self.instance.id}-{field}',
            'hx-trigger': 'keyup delay:500ms, change delay:500ms',
            'onkeydown': 'showLoadingSpinner(this)',
            'onchange': 'showLoadingSpinner(this)',
            'hx-on::after-request': 'hideLoadingSpinner(this)',
            'hx-swap': 'outerHTML',
        })
        self.fields['member'].widget.attrs.update({
            'value': self.instance.member.pk,
        })
        self.fields['prev_value'].widget.attrs.update({
            'value': getattr(self.instance, field),
        })

class FamilyMemberNameForm(FamilyMemberBaseForm):
    class Meta:
        model = FamilyMember
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class FamilyMemberDateOfBirthForm(FamilyMemberBaseForm):
    class Meta:
        model = FamilyMember
        fields = ['date_of_birth']
        widgets = {'date_of_birth': DateInput(attrs={'class': 'form-control'})}

class FamilyMemberRelationshipForm(FamilyMemberBaseForm):
    class Meta:
        model = FamilyMember
        fields = ['relationship']
        widgets = {'relationship': forms.Select(attrs={'class': 'form-control'})}
        labels = {'relationship': 'Rel.'}

class FamilyMemberCategoryInterest1Form(FamilyMemberBaseForm):
    class Meta:
        model = FamilyMember
        fields = ['category_interest_1']
        widgets = {'category_interest_1': forms.Select(attrs={'class': 'form-control'})}
        labels = {'category_interest_1': 'Interest 1'}

class FamilyMemberCategoryInterest2Form(FamilyMemberBaseForm):
    class Meta:
        model = FamilyMember
        fields = ['category_interest_2']
        widgets = {'category_interest_2': forms.Select(attrs={'class': 'form-control'})}
        labels = {'category_interest_2': 'Interest 2'}

class FamilyMemberCategoryInterest3Form(FamilyMemberBaseForm):
    class Meta:
        model = FamilyMember
        fields = ['category_interest_3']
        widgets = {'category_interest_3': forms.Select(attrs={'class': 'form-control'})}
        labels = {'category_interest_3': 'Interest 3'}


FORM_MAPPER = {
    'name': FamilyMemberNameForm,
    'date_of_birth': FamilyMemberDateOfBirthForm,
    'relationship': FamilyMemberRelationshipForm,
    'category_interest_1': FamilyMemberCategoryInterest1Form,
    'category_interest_2': FamilyMemberCategoryInterest2Form,
    'category_interest_3': FamilyMemberCategoryInterest3Form
}
        