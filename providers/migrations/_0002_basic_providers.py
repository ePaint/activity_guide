# Generated by Django 4.2.7 on 2023-12-20 13:22

import os
import random
from django.conf import settings
from django.db import migrations
from dotenv import load_dotenv

load_dotenv(override=True)


class Migration(migrations.Migration):

    def custom_task(apps, schema_editor):
        to_create = [
            {
                "name": "Playful Learning Academy",
                "slug": "playful-learning",
                "description": "Engaging educational activities for kids, fostering creativity, curiosity, and a love for learning in a playful environment."
            },
            {
                "name": "Artistic Explorers Studio",
                "slug": "artistic-explorers",
                "description": "Art-focused provider offering hands-on activities for kids to explore various artistic mediums, encouraging self-expression and imagination."
            },
            {
                "name": "Nature Discovery Club",
                "slug": "nature-discovery",
                "description": "Outdoor adventures and nature-based activities for kids, promoting environmental awareness, exploration, and a connection to the natural world."
            },
            {
                "name": "Fun Fitness Friends",
                "slug": "fun-fitness",
                "description": "Kid-friendly fitness programs and activities to instill healthy habits, teamwork, and the joy of physical activity in a fun and supportive setting."
            },
            {
                "name": "Science Wonders Lab",
                "slug": "science-wonders",
                "description": "Exciting and interactive science activities for kids, sparking curiosity and a love for discovery through hands-on experiments and exploration."
            },
            {
                "name": "Storybook Adventures Club",
                "slug": "storybook-adventures",
                "description": "Immersive storytelling experiences and activities for kids, fostering a love for literature, creativity, and imaginative play."
            },
            {
                "name": "Musical Melodies School",
                "slug": "musical-melodies",
                "description": "Musical education and activities for kids, introducing them to the joy of music, rhythm, and creative expression through instruments and singing."
            },
            {
                "name": "Tech Tots Coding Hub",
                "slug": "tech-tots-coding",
                "description": "Introduction to coding and technology for kids, offering interactive and age-appropriate activities to develop early STEM skills."
            },
            {
                "name": "Super Chef Junior Kitchen",
                "slug": "super-chef-junior",
                "description": "Cooking and culinary activities for kids, encouraging creativity in the kitchen, healthy eating habits, and a love for food exploration."
            },
            {
                "name": "Adventure Seekers Club",
                "slug": "adventure-seekers",
                "description": "Outdoor adventure activities for kids, promoting teamwork, resilience, and a sense of exploration through nature-based challenges."
            },
            {
                "name": "Crafty Creations Workshop",
                "slug": "crafty-creations",
                "description": "Craft and DIY activities for kids, providing a platform for creative expression, fine motor skills development, and artistic exploration."
            },
            {
                "name": "Dance Magic Studio",
                "slug": "dance-magic",
                "description": "Fun and expressive dance activities for kids, fostering coordination, rhythm, and a love for movement in a positive and inclusive environment."
            },
            {
                "name": "Little Athlete Training Camp",
                "slug": "little-athlete",
                "description": "Sports and athletic activities for kids, promoting physical fitness, sportsmanship, and teamwork through age-appropriate games and exercises."
            },
            {
                "name": "Animal Safari Explorers",
                "slug": "animal-safari",
                "description": "Wildlife-themed activities for kids, offering an educational and interactive exploration of animals, habitats, and conservation."
            },
            {
                "name": "Magical Imagination Theater",
                "slug": "imagination-theater",
                "description": "Theater and drama activities for kids, encouraging creativity, self-expression, and confidence through imaginative play and storytelling."
            },
            {
                "name": "Little Gardeners Club",
                "slug": "little-gardeners",
                "description": "Gardening activities for kids, promoting environmental awareness, responsibility, and a connection to nature through hands-on gardening experiences."
            },
            {
                "name": "Junior Yoga Harmony",
                "slug": "junior-yoga-harmony",
                "description": "Yoga and mindfulness activities for kids, fostering balance, relaxation, and emotional well-being through gentle movement and mindfulness practices."
            },
            {
                "name": "Math Wizards Learning Center",
                "slug": "math-wizards",
                "description": "Mathematics-focused activities for kids, making learning fun and engaging through interactive games, puzzles, and mathematical exploration."
            },
            {
                "name": "Playtime Language Explorers",
                "slug": "language-explorers",
                "description": "Language learning activities for kids, introducing them to new languages and cultures through play, songs, and interactive language activities."
            },
            {
                "name": "Robot Builders Workshop",
                "slug": "robot-builders",
                "description": "Robotics and engineering activities for kids, fostering creativity and problem-solving skills through hands-on building and programming."
            }
        ]
        
        random_urls = [
            'https://www.google.com',
            'https://www.youtube.com',
            'https://www.facebook.com',
            'https://www.twitter.com',
            'https://www.instagram.com',
            'https://www.linkedin.com',
            'https://www.pinterest.com',
            'https://www.tiktok.com',
            'https://www.snapchat.com',
            'https://www.reddit.com',
            'https://www.tumblr.com',
            'https://www.flickr.com',
            'https://www.whatsapp.com',
        ]

        Provider = apps.get_model('providers', 'Provider')

        image_prefix = f'https://{os.getenv('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com'
        print(image_prefix)

        for provider in to_create:
            Provider.objects.create(
                name=provider['name'],
                email='example@example.com',
                phone='4165557890',
                slug=provider['slug'],
                description=provider['description'],
                image=f'providers/{provider['slug']}.jpg',
                url=random.choice(random_urls),
                is_featured=random.choice([True, False, False, False, False]),
            )
        

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(custom_task, migrations.RunPython.noop),
    ]