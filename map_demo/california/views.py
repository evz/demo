from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.gis.geos import Point, Polygon
import json
import requests
from california.models import *

def counties(request):
    counties = County.objects.all()
    return render_to_response('basic-county.html', {'counties': counties}, context_instance=RequestContext(request))
    
def places(request):
    places = Place.objects.all()
    return render_to_response('basic-place.html', {'places': places}, context_instance=RequestContext(request))

def complex_county(request):
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

def tiles_county(request):
    counties = County.objects.all()
    bbox = json.dumps(counties.extent())
    return render_to_response('tiles-county.html', { 'bbox': bbox }, context_instance=RequestContext(request))

def map_search(request, template=None):
    counties = County.objects.all()
    places = Place.objects.all()
    bbox = json.dumps(counties.extent())
    if request.path == '/census/':
        template = 'census.html'
    else:
        template = 'map-search.html'
    if request.is_ajax():
        q = request.GET['search']
        goog = 'http://maps.googleapis.com/maps/api/geocode/json'
        r = requests.get(goog, params={'address': q, 'sensor': 'false'});
        resp = json.loads(r.content)
        d = {'status': resp['status']}
        if resp['status'] != 'OK':
            d['message'] = 'Nothing was found matching your search. Please try again.'
        elif len(resp['results']) > 1:
            clarify = []
            for res in resp['results']:
                clarify.append(res['formatted_address'])
            d['status'] = 'MULTIPLE_MATCHES'
            d['message'] = 'Did you mean one of these? Click the one you wanted to resubmit.'
            d['clarify'] = clarify 
        else:
            bounds = resp['results'][0]['geometry']['viewport']
            bbox = (bounds['southwest']['lng'], bounds['southwest']['lat'], bounds['northeast']['lng'], bounds['northeast']['lat'])
            bbox_poly = Polygon.from_bbox(bbox)
            cnts = counties.filter(mpoly__bboverlaps=bbox_poly)
            plcs = places.filter(mpoly__bboverlaps=bbox_poly)
            c = []
            p = []
            for cnt in cnts.geojson():
                geojson = json.loads(cnt.geojson)
                geojson['properties'] = {
                    'name': cnt.name_trans,
                    'bbox': cnt.mpoly.extent,
                    'center':cnt.mpoly.point_on_surface.coords
                    }
                geojson['id'] = cnt.geo_id
                c.append(geojson)
            d['counties'] = c
            for plc in plcs.geojson():
                geojson = json.loads(plc.geojson)
                geojson['properties'] = {
                    'name': plc.name_trans,
                    'bbox': plc.mpoly.extent,
                    'center':plc.mpoly.point_on_surface.coords
                    }
                geojson['id'] = plc.geo_id
                p.append(geojson)
            d['places'] = p
        return HttpResponse(json.dumps(d), mimetype='application/json')
    else:
        return render_to_response(template, { 'bbox': bbox }, context_instance=RequestContext(request))
