from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.auth.models import User

from autoslug import AutoSlugField
from django_extensions.db import fields as ext_fields


# __author__ = 'Sourav Banerjee'
# __email__ = ' srvasn@gmail.com'

class Region(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', max_length=255)
    uuid = ext_fields.UUIDField(auto=True)
    creator = models.ForeignKey('auth.User', related_name='regions', default='1')
    # Geo Django field to store a polygon
    area = models.PolygonField()
    price = models.IntegerField()

    # You MUST use GeoManager to make Geo Queries
    objects = models.GeoManager()


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',
                                help_text='User associated with Vendor')
    name = models.CharField(max_length=255, help_text='Name of the vendor')
    phone = models.CharField(max_length=15, help_text='Phone number of the vendor')
    lang = models.CharField(max_length=20, help_text='Language preferred by the vendor')
    curr = models.CharField(max_length=3, help_text='Transaction currency preferred.')
