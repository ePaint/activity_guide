# Generated by Django 4.2.7 on 2023-12-19 11:42

from django.db import migrations, models
import django.db.models.deletion


LOCATIONS = [
    ('Kamloops', 'Kamloops'),
    ('Aberdeen', 'Aberdeen'),
    ('Batchlor Heights', 'Batchlor Heights'),
    ('Barnhartvale', 'Barnhartvale'),
    ('Brocklehurst', 'Brocklehurst'),
    ('Campble Creek', 'Campble Creek'),
    ('Dallas', 'Dallas'),
    ('Downtown', 'Downtown'),
    ('Harper Mountain', 'Harper Mountain'),
    ('Juniper Ridge', 'Juniper Ridge'),
    ('McArthur Island', 'McArthur Island'),
    ('North Kamloops', 'North Kamloops'),
    ('Rayleigh / Heffley', 'Rayleigh / Heffley'),
    ('Sahali Upper', 'Sahali Upper'),
    ('Sahali Lower', 'Sahali Lower'),
    ('Sun Peaks', 'Sun Peaks'),
    ('TRU', 'TRU'),
    ('Valleyview', 'Valleyview'),
    ('Westsyde', 'Westsyde'),
]

ACTIVITY_TYPES = [
    ('Indoor', 'Indoor'),
    ('Outdoor', 'Outdoor'),
    ('Mixed', 'Mixed'),
]


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='activities')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category', related_name='activities')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='providers.provider', related_name='activities')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('weekday', models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=20, null=True)),
                ('age_start', models.IntegerField()),
                ('age_end', models.IntegerField(blank=True, null=True)),
                ('position', models.CharField(blank=True, max_length=20, null=True)),
                ('location', models.CharField(blank=True, choices=LOCATIONS, max_length=20, null=True)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('price_period', models.CharField(choices=[('day', 'day'), ('week', 'week'), ('month', 'month'), ('year', 'year')], max_length=20)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('activity_type', models.CharField(choices=ACTIVITY_TYPES, max_length=20)),
                ('is_visually_adaptive', models.BooleanField(default=False)),
                ('is_hearing_adaptive', models.BooleanField(default=False)),
                ('is_mobility_adaptive', models.BooleanField(default=False)),
                ('is_cognitive_adaptive', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
                'ordering': ['created_at'],
            },
        ),
    ]
