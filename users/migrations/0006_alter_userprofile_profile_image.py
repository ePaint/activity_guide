# Generated by Django 4.2.7 on 2023-11-29 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_userprofile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='', upload_to='profile_images'),
        ),
    ]
