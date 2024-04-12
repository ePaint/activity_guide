from django.shortcuts import render
from ads.forms import AdForm
from .models import Ad, AD_LOCATIONS
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def home(request):
    if request.method == 'POST':
        ad_form = AdForm(request.POST, request.FILES, instance=request.user)
        context = {
            'ad_form': ad_form,
        }
        if ad_form.is_valid():
            ad_form.save()
            response = render(request, 'ads/home.html', context)
            return response
    else: 
        sections = []

        for location in AD_LOCATIONS:
            ads = Ad.objects.filter(location=location[0])
            forms = [AdForm(instance=ad) for ad in ads]

            for _ in range(8 - len(forms)):
                forms.append(AdForm())
            sections.append({
                'title': location[1],
                'forms': forms,
            })

    context = {
        'sections': sections,
    }
    return render(request, 'ads/home.html', context)
