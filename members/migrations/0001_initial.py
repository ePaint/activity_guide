# Generated by Django 4.2.7 on 2024-01-22 19:59

import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0002_basic_offers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member', to=settings.AUTH_USER_MODEL)),
                ('liked_activities', models.ManyToManyField(related_name='liked_by', to='activities.activity', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
                'db_table': 'member',
            },
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('relationship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family_members', to='members.relationship')),
                ('activities', models.ManyToManyField(to='activities.activity', related_name='family_members', blank=True, null=True)),
                ('category_interest_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_interest_1', to='categories.Category')),
                ('category_interest_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_interest_2', to='categories.Category')),
                ('category_interest_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_interest_3', to='categories.Category')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member', related_name='family_members')),
            ],
            options={
                'verbose_name': 'Family Member',
                'verbose_name_plural': 'Family Members',
                'db_table': 'family_member',
                'ordering': ['date_of_birth'],
            },
        ),
    ]
