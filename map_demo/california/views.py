from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json
from california.models import *

def counties(request):
    counties = County.objects.all()
    return render_to_response('basic-county.html', {'counties': counties}, context_instance=RequestContext(request))
    
def places(request):
    places = Place.objects.all()
    return render_to_response('basic-place.html', {'places': places}, context_instance=RequestContext(request))

def complex_counties(request):
    counties = County.objects.all()
    bbox = json.dumps(counties.extent())
    if request.is_ajax():
        d = {}
        for county in counties.geojson():
            geojson = json.loads(county.geojson)
            properties = {'name': county.name_trans, 'bbox':county.mpoly.extent, 'center':county.mpoly.point_on_surface.coords}
            geojson['id'] = county.geo_id
            geojson['properties'] = properties
            d[county.geo_id] = geojson 
        return HttpResponse(json.dumps(d), mimetype='application/json')
    else:
        return render_to_response('complex-county.html', { 'bbox': bbox }, context_instance=RequestContext(request))
