#!/usr/bin/env python

# For this script to work we must set the Django settings file
# as an environment setting before importing LayerMapping

# Alternatively you can place 
# export DJANGO_SETTINGS_MODULE=settings
# in your .bash_profile
#
# or paste this code into a $ manage.py shell

import sys
import site
import os
vepath = '/home/web/sites/demo/lib/python2.7/site-packages'
prev_sys_path = list(sys.path)
# add the site-packages of our virtualenv as a site dir
site.addsitedir(vepath)
sys.path.append('/home/web/sites/demo/map_demo')
sys.path.append('/home/web/sites/demo/')

new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
sys.path[:0] = new_sys_path

os.environ['DJANGO_SETTINGS_MODULE'] = 'map_demo.settings'

from psycopg2 import IntegrityError

from django.contrib.gis.utils import mapping, LayerMapping, add_postgis_srs
from map_demo.california.models import County, Place

try:
    add_postgis_srs(900913)
except IntegrityError:
    print "The Google Spherical Mercator projection, or a projection with srid 900913, already exists, skipping insert"


County_shp = '/home/web/sites/demo/data/county/tl_2010_06_county10.shp'
Place_shp = '/home/web/sites/demo/data/place/tl_2010_06_place10.shp'

County_mapping = {
        'state_fips'  : 'STATEFP10',
        'county_fips'  : 'COUNTYFP10',
        'county_ansi'	: 'COUNTYNS10',
        'geo_id' : 'GEOID10',
        'name' : 'NAME10',
        'name_trans' : 'NAMELSAD10',
        'mpoly' : 'MULTIPOLYGON',
}

Place_mapping = {
        'state_fips'  : 'STATEFP10',
        'place_fips'  : 'PLACEFP10',
        'place_ansi'	: 'PLACENS10',
        'geo_id' : 'GEOID10',
        'name' : 'NAME10',
        'name_trans' : 'NAMELSAD10',
        'mpoly' : 'MULTIPOLYGON',
}

County_layer = LayerMapping(County,
                      County_shp,
                      County_mapping,
                      transform=False,
                      encoding='iso-8859-1')

County_layer.save(verbose=True, strict=True, progress=True)

Place_layer = LayerMapping(Place,
                    Place_shp,
                    Place_mapping,
                    transform=False,
                    encoding='iso-8859-1')

Place_layer.save(verbose=True, strict=True, progress=True)