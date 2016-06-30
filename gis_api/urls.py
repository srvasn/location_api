from django.conf.urls import url

from gis_api import views

# __author__ = 'Sourav Banerjee'
# __email__ = ' srvasn@gmail.com'

urlpatterns = [
    url(r'^vendors/account$', views.auth_view, name='vendors-profile'),
    url(r'^vendors/$', views.user_view, name='vendors-list'),
    url(r'^vendors/(?P<pk>[0-9]+)/$', views.user_detail, name='vendors-detail'),
    url(r'^regions/contains/$', views.point_in_region, name='point-in-region'),
    url(r'^regions/$', views.region_list, name='region-list'),
    url(r'^regions/(?P<pk>[0-9]+)/$', views.region_detail, name='region-update'),
]
