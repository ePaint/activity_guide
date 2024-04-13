import copy
from django.shortcuts import render
from activity_guide.settings import MAX_ADS_PER_SECTION
from ads.forms import MODEL_FORM_SETS
from .models import AD_LOCATIONS, AD_SIZES
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def home(request):
    sections = []

    index = 0
    for location_code, location_label in AD_LOCATIONS.items():
        ad_form_set = MODEL_FORM_SETS[location_code]
        ad_dimensions = AD_SIZES[location_code]
        index += 1
        sections.append({
            'title': location_label,
            'location': location_code,
            'forms': ad_form_set(),
            'width': ad_dimensions['width'],
            'height': ad_dimensions['height'],
        })
    
    context = {
        'sections': sections,
    }
    return render(request, 'ads/home.html', context)

@staff_member_required
def save(request, location):    
    AdFormSet = MODEL_FORM_SETS[location]
    data = copy.deepcopy(request.POST)
    data['form-TOTAL_FORMS'] = MAX_ADS_PER_SECTION
    data['form-INITIAL_FORMS'] = MAX_ADS_PER_SECTION
    formset = AdFormSet(data, request.FILES)
    
    if formset.is_valid():
        print('Saving formset')
        formset.save()

    context = {
        'title': AD_LOCATIONS[location],
        'location': location,
        'forms': MODEL_FORM_SETS[location](),
    }
    
    return render(request, 'ads/partials/form.html', context)