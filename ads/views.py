import copy
from django.shortcuts import render
from activity_guide.settings import MAX_ADS_PER_SECTION
from ads.forms import MODEL_FORM_SETS
from .models import AD_LOCATIONS, AD_SIZES
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def home(request):
    sections = []
    for location_code, location_label in AD_LOCATIONS.items():
        ad_form_set = MODEL_FORM_SETS[location_code]
        ad_dimensions = AD_SIZES[location_code]
        sections.append({
            'title': location_label,
            'location': location_code,
            'forms': ad_form_set(),
            'desktop_width': ad_dimensions['desktop']['width'],
            'desktop_height': ad_dimensions['desktop']['height'],
            'mobile_width': ad_dimensions['mobile']['width'],
            'mobile_height': ad_dimensions['mobile']['height'],
        })
    
    context = {
        'sections': sections,
    }
    return render(request, 'ads/home.html', context)

@staff_member_required
def save(request, location):
    ad_form_set = MODEL_FORM_SETS[location]
    ad_dimensions = AD_SIZES[location]
    data = copy.deepcopy(request.POST)
    data['form-TOTAL_FORMS'] = MAX_ADS_PER_SECTION
    data['form-INITIAL_FORMS'] = MAX_ADS_PER_SECTION
    formset = ad_form_set(data, request.FILES)
    
    if formset.is_valid():
        formset.save()

    context = {
        'title': AD_LOCATIONS[location],
        'location': location,
        'forms': MODEL_FORM_SETS[location](),
        'desktop_width': ad_dimensions['desktop']['width'],
        'desktop_height': ad_dimensions['desktop']['height'],
        'mobile_width': ad_dimensions['mobile']['width'],
        'mobile_height': ad_dimensions['mobile']['height'],
    }
    
    return render(request, 'ads/partials/form.html', context)