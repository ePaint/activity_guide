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
                "image_desktop": "ads/home_page.jpg",
                "image_mobile": "ads/home_page_mobile.jpg",
                "location": "H",
                "click_action": "Open URL",
                "click_action_target": "https://www.bcwildlife.com",
            },
            
            {
                "image_desktop": "ads/search_results_1.png",
                "image_mobile": "ads/search_results_1_mobile.png",
                "location": "S",
                "click_action": "Open URL",
                "click_action_target": "https://raregroupkamloops.ca/",
            },
            
            {
                "image_desktop": "ads/search_results_2.png",
                "image_mobile": "ads/search_results_2_mobile.jpg",
                "location": "S1",
                "click_action": "Send Email",
                "click_action_target": "marketing@activityguide.ca",
            },
            
            {
                "image_desktop": "ads/search_results_3.png",
                "image_mobile": "ads/search_results_3_mobile.jpg",
                "location": "S2",
                "click_action": "Open URL",
                "click_action_target": "https://khykhythelabel.com/",
            },       
            
            {
                "image_desktop": "ads/categories_1.png",
                "location": "C1",
                "click_action": "Send Email",
                "click_action_target": "marketing@activityguide.ca",
            },
            
            {
                "image_desktop": "ads/categories_2.png",
                "image_mobile": "ads/categories_2_mobile.jpg",
                "location": "C2",
                "click_action": "Open URL",
                "click_action_target": "https://route1distillery.ca/",
            },
            
            {
                "image_desktop": "ads/categories_3.png",
                "location": "C3",
                "click_action": "Open URL",
                "click_action_target": "https://www.facebook.com/ConsignorSports",
            },
            
            {
                "image_desktop": "ads/arts.png",
                "image_mobile": "ads/arts_mobile.jpg",
                "location": "ARTS",
                "click_action": "Open URL",
                "click_action_target": "https://wctlive.ca/thehub/default.htm",
            },
            
            {
                "image_desktop": "ads/sports.png",
                "image_mobile": "ads/sports_mobile.png",
                "location": "SPORTS",
                "click_action": "Open URL",
                "click_action_target": "https://kamloopsminorhockey.com/registration/",
            },
            
            {
                "image_desktop": "ads/stem.png",
                "image_mobile": "ads/stem_mobile.png",
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
                image_desktop=ad['image_desktop'],
                image_mobile=ad.get('image_mobile'),
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
                    image_desktop=None,
                    image_mobile=None,
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
