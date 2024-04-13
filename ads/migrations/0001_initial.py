# Generated by Django 4.2.7 on 2024-04-12 22:38

from django.db import migrations, models

AD_LOCATIONS = {
    'H': 'Homepage Top Ads',
    'S': 'Search Results Top Ads',
    'S1': 'Search Results Sidebar #1 Ads',
    'S2': 'Search Results Sidebar #2 Ads',
    'C1': 'Categories Top-left Ads',
    'C2': 'Categories Top-middle Ads',
    'C3': 'Categories Top-right Ads',
    'ARTS': 'Arts Category Sidebar Ads',
    'SPORTS': 'Sports Category Sidebar Ads',
    'STEM': 'STEM Category Sidebar Ads',
}

AD_CLICK_ACTIONS = {
    'Open URL': 'Open URL',
    'Send Email': 'Send Email',
}

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=AD_LOCATIONS.items(), max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='AdClickAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=AD_CLICK_ACTIONS.items(), max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('location', models.ForeignKey(on_delete=models.CASCADE, to='ads.AdLocation', related_name='ads')),
                ('click_action', models.ForeignKey(on_delete=models.CASCADE, to='ads.AdClickAction', related_name='ads', blank=True, null=True)),
                ('click_action_target', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
