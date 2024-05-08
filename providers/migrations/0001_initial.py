# Generated by Django 4.2.7 on 2023-12-20 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField()),
                ('phone', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='providers')),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=models.CASCADE, related_name='provider', to='users.User')),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Providers',
                'ordering': ['created_at'],
            },
        ),
    ]
