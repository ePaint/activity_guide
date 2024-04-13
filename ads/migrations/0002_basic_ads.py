# Generated by Django 4.2.7 on 2023-12-20 13:22
from activity_guide.settings import MAX_ADS_PER_SECTION
from django.db import migrations
from dotenv import load_dotenv

load_dotenv(override=True)


class Migration(migrations.Migration):

    def custom_task(apps, schema_editor):
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
        
        ads_to_create = [
            {
                "image_url": "ads/home_page.jpg",
                "location": "H",
                "click_action": "Open URL",
                "click_action_target": "https://www.bcwildlife.com",
            },
            
            {
                "image_url": "ads/search_results_1.png",
                "location": "S",
                "click_action": "Open URL",
                "click_action_target": "https://raregroupkamloops.ca/",
            },
            
            {
                "image_url": "ads/search_results_2.png",
                "location": "S1",
                "click_action": "Send Email",
                "click_action_target": "marketing@activityguide.ca",
            },
            
            {
                "image_url": "ads/search_results_3.png",
                "location": "S2",
                "click_action": "Open URL",
                "click_action_target": "https://khykhythelabel.com/",
            },       
            
            {
                "image_url": "ads/categories_1.png",
                "location": "C1",
                "click_action": "Send Email",
                "click_action_target": "marketing@activityguide.ca",
            },
            
            {
                "image_url": "ads/categories_2.png",
                "location": "C2",
                "click_action": "Open URL",
                "click_action_target": "https://route1distillery.ca/",
            },
            
            {
                "image_url": "ads/categories_3.png",
                "location": "C3",
                "click_action": "Open URL",
                "click_action_target": "https://www.facebook.com/ConsignorSports",
            },
            
            {
                "image_url": "ads/arts.png",
                "location": "ARTS",
                "click_action": "Open URL",
                "click_action_target": "https://wctlive.ca/thehub/default.htm",
            },
            
            {
                "image_url": "ads/sports.png",
                "location": "SPORTS",
                "click_action": "Open URL",
                "click_action_target": "https://kamloopsminorhockey.com/registration/",
            },
            
            {
                "image_url": "ads/stem.png",
                "location": "STEM",
                "click_action": "Send Email",
                "click_action_target": "marketing@activityguide.ca",
            }
        ]
        
        AdLocation = apps.get_model('ads', 'AdLocation')
        for location in AD_LOCATIONS.keys():
            AdLocation.objects.create(
                location=location,
            )
            
        AdClickAction = apps.get_model('ads', 'AdClickAction')
        for action in AD_CLICK_ACTIONS.keys():
            AdClickAction.objects.create(
                action=action,
            )
        
        Ad = apps.get_model('ads', 'Ad')
        for ad in ads_to_create:
            Ad.objects.create(
                image=ad['image_url'],
                location=AdLocation.objects.get(location=ad['location']),
                click_action=AdClickAction.objects.get(action=ad.get('click_action')) if ad.get('click_action') else None,
                click_action_target=ad['click_action_target'],
            )
        
        for location in AD_LOCATIONS.keys():
            count = Ad.objects.filter(location__location=location).count()
            
            if count >= MAX_ADS_PER_SECTION:
                continue
            
            Ad.objects.bulk_create([
                Ad(
                    image=None,
                    location=AdLocation.objects.get(location=location),
                    click_action=None,
                    click_action_target=None,
                ) for _ in range(MAX_ADS_PER_SECTION - count)
            ])


    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(custom_task, migrations.RunPython.noop),
    ]
