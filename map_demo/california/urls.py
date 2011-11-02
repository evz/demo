from django.conf.urls.defaults import *

from california.views import *

urlpatterns = patterns('',
    url(r'^counties/$', counties, name='counties'),
    url(r'^places/$', places, name='places'),
    url(r'^complex-county/$', complex_county, name='complex-county'),
    url(r'^tiles-county/$', tiles_county, name='tiles-county'),
    url(r'^map-search/$', map_search, name='map-search'),
    url(r'^census/$', map_search, name='map-search'),
)