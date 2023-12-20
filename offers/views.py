from django.shortcuts import render
from offers.models import Offer


def offer_detail(request, slug):
    offer = Offer.objects.get(slug=slug)
    context = {
        'offer': offer
    }
    return render(request, 'offers/offer_detail.html', context)
