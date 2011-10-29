from django.contrib.gis.db import models

class County(models.Model):
    state_fips = models.CharField(max_length=10)
    county_fips = models.CharField(max_length=10)
    county_ansi = models.CharField(max_length=10)
    geo_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    name_trans = models.CharField(max_length=100)
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
        
class Place(models.Model):
    state_fips = models.CharField(max_length=10)
    place_fips = models.CharField(max_length=10)
    place_ansi = models.CharField(max_length=10)
    geo_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    name_trans = models.CharField(max_length=100)
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name