# Generated by Django 4.2.7 on 2023-12-18 22:11

from django.db import migrations


class Migration(migrations.Migration):

    # Creates 3 basic categories: Sports, Art, and Science
    def custom_task(self, schema_editor):
        Category = self.get_model('categories', 'Category')

        to_create = [
            {
                "name": "Sports",
                "description": "Sports are all forms of usually competitive physical activity or games which, through casual or organized participation, aim to use, maintain or improve physical ability and skills while providing enjoyment to participants, and in some cases, entertainment for spectators.",
                "slug": "sports",
                "parent": None
            },
            {
                "name": "Art",
                "description": "Art is a diverse range of human activities involving the creation of visual, auditory or performing artifacts (artworks), which express the creator's imagination, conceptual ideas, or technical skill, intended to be appreciated primarily for their beauty or emotional power.",
                "slug": "art",
                "parent": None
            },
            {
                "name": "STEM",
                "description": "STEM (Science, Technology, Engineering, and Mathematics) is a comprehensive and interdisciplinary approach to learning and problem-solving. It brings together the principles and methodologies of science, technology, engineering, and mathematics to address real-world challenges.",
                "slug": "stem",
                "parent": None
            },
            {
                "name": "Soccer",
                "description": "Soccer is a popular team sport that is played and loved by millions around the world. It involves two teams trying to score goals by getting a ball into the opposing team's net.",
                "slug": "soccer",
                "parent": "sports"
            },
            {
                "name": "Hockey",
                "description": "Hockey is a popular team sport that is played and loved by millions around the world. It involves two teams trying to score goals by getting a puck into the opposing team's net.",
                "slug": "hockey",
                "parent": "sports"
            },
            {
                "name": "Baseball",
                "description": "Baseball is a popular team sport that is played and loved by millions around the world. It involves two teams trying to score runs by hitting a ball with a bat and touching a series of four bases arranged at the corners of a ninety-foot diamond.",
                "slug": "baseball",
                "parent": "sports"
            },
            {
                "name": "Horseback Riding",
                "description": "Horseback riding is a popular sport that is played and loved by millions around the world. It involves riding a horse. It is also known as equestrianism.",
                "slug": "horseback-riding",
                "parent": "sports"
            },
            {
                "name": "Cheer",
                "description": "Cheer is a popular team sport that is played and loved by millions around the world. It involves two teams trying to score points by performing routines that include stunts, jumps, tumbling, and dance.",
                "slug": "cheer",
                "parent": "sports"
            },
            {
                "name": "Golf",
                "description": "Golf is a popular individual sport that is played and loved by millions around the world. It involves hitting a ball with a club into a series of holes on a course in as few strokes as possible.",
                "slug": "golf",
                "parent": "sports"
            },
            {
                "name": "Swimming",
                "description": "Swimming is a popular individual sport that is played and loved by millions around the world. It involves moving through water by using the limbs, usually the arms and legs.",
                "slug": "swimming",
                "parent": "sports"
            },
            {
                "name": "Diving",
                "description": "Diving is a popular individual sport that is played and loved by millions around the world. It involves jumping or falling into water from a platform or springboard.",
                "slug": "diving",
                "parent": "sports"
            },
            {
                "name": "Mountain Biking",
                "description": "Mountain biking is a popular individual sport that is played and loved by millions around the world. It involves riding a bicycle off-road, often over rough terrain.",
                "slug": "mountain-biking",
                "parent": "sports"
            },
            {
                "name": "Gymnastics",
                "description": "Gymnastics is a popular individual sport that is played and loved by millions around the world. It involves performing exercises that require balance, strength, flexibility, agility, coordination, and endurance.",
                "slug": "gymnastics",
                "parent": "sports"
            },
            {
                "name": "Tennis",
                "description": "Tennis is a popular individual sport that is played and loved by millions around the world. It involves hitting a ball with a racket over a net into the opponent's court.",
                "slug": "tennis",
                "parent": "sports"
            },
            {
                "name": "Theatre",
                "description": "Theatre is a popular art form that is enjoyed by millions around the world. It involves performing a play, musical, or other dramatic work.",
                "slug": "theatre",
                "parent": "art"
            },
            {
                "name": "Dance",
                "description": "Dance is a popular art form that is enjoyed by millions around the world. It involves moving rhythmically to music, typically following a set sequence of steps.",
                "slug": "dance",
                "parent": "art"
            },
            {
                "name": "Sculpting",
                "description": "Sculpting is a popular art form that is enjoyed by millions around the world. It involves creating a three-dimensional work of art by carving, modeling, or casting.",
                "slug": "sculpting",
                "parent": "art"
            },
            {
                "name": "Drawing",
                "description": "Drawing is a popular art form that is enjoyed by millions around the world. It involves making marks on a surface by applying pressure from a tool, usually a pencil or pen.",
                "slug": "drawing",
                "parent": "art"
            },
            {
                "name": "Painting",
                "description": "Painting is a popular art form that is enjoyed by millions around the world. It involves applying paint, pigment, or other medium to a surface with a brush.",
                "slug": "painting",
                "parent": "art"
            }
        ]

        for item in to_create:
            parent_slug = item.get('parent')
            parent = Category.objects.get(slug=parent_slug) if parent_slug else None
            Category.objects.get_or_create(
                name=item.get('name'),
                description=item.get('description'),
                slug=item.get('slug'),
                parent=parent
            )

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(custom_task, migrations.RunPython.noop),
    ]
