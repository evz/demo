from django.shortcuts import render_to_response
from django.template import RequestContext
from california.models import *

def counties(request):
    counties = County.objects.all()
    return render_to_response('basic-county.html', {'counties': counties}, context_instance=RequestContext(request))
    
def places(request):
    places = Place.objects.all()
    return render_to_response('basic-place.html', {'places': places}, context_instance=RequestContext(request))
