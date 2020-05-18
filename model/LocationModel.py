from django.db import models
from django.contrib.gis.db import models as models_gis

class Location(models.Model):
    location_id = models.BigAutoField(primary_key=True, blank=False)
    place_id = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255 ,blank=False)
    coordinates = models_gis.GeometryField(blank=False)
    category = models.IntegerField(default=0, blank=False)
    # rating = models.FloatField(default=0, blank=False)
    # api에서 제공 X
    # used_time = models.FloatField(default=0, blank=False) # doulbe??
    image = models.CharField(max_length=1000, null=True, blank=False, default="no image")

    # 튜플의 대표값
    def __str__(self):
        return self.name