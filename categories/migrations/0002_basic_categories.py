# Generated by Django 4.2.7 on 2023-12-18 22:11

from django.db import migrations


class Migration(migrations.Migration):

    # Creates 3 basic categories: Sports, Art, and Science
    def custom_task(self, schema_editor):
        Category = self.get_model('categories', 'Category')
        
        to_create = [
            {
                'name': 'Sports',
                'description': 'Sports are all forms of usually competitive physical activity or games which, through casual or organized participation, aim to use, maintain or improve physical ability and skills while providing enjoyment to participants, and in some cases, entertainment for spectators.',
                'slug': 'sports',
            },
            {
                'name': 'Art',
                'description': 'Art is a diverse range of human activities involving the creation of visual, auditory or performing artifacts (artworks), which express the creator\'s imagination, conceptual ideas, or technical skill, intended to be appreciated primarily for their beauty or emotional power.',
                'slug': 'art',
            },
            {
                'name': 'Science',
                'description': 'Science is a systematic enterprise that builds and organizes knowledge in the form of testable explanations and predictions about the universe.',
                'slug': 'science',
            },
        ]
        
        for item in to_create:
            Category.objects.get_or_create(**item)


    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(custom_task, migrations.RunPython.noop),
    ]