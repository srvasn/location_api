from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry

from gis_api.models import Region
from gis_api.serializers import RegionSerializer, UserSerializer
from gis_api.permissions import IsStaffOrTargetUser, IsOwnerOrReadOnly
from gis_api.authentication import QuietBasicAuthentication

# __author__ = 'Sourav Banerjee'
# __email__ = ' srvasn@gmail.com'

class AuthView(APIView):
    """
    Used to authenticate users using Basic HTTP Authentication, with credentials in header
    """
    authentication_classes = (QuietBasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        #returning username on successful registration
        return Response(self.serializer_class(request.user).data)


class UserView(viewsets.ModelViewSet):
    """
    Vendor registration, retrieve, update, delete.
    GET, PUT and DELETE on this view work for staff only.
    POST is allowed for Anonymous users for registration.
    """
    serializer_class = UserSerializer
    model = get_user_model()
    queryset = model.objects.all()

    def get_permissions(self):
        # Let anonymous users POST, but not retrieve all/update/delete
        if self.request.method == 'POST':
            return (AllowAny(),)
        else:
            return (IsStaffOrTargetUser(),)

class RegionList(generics.ListCreateAPIView):
    """
    POST to create a new Region, GET for a list (authentication required).
    Area has to be a polygon in GeoJSON format.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = RegionSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = Region.objects.all()
        else:
            queryset = Region.objects.filter(creator=self.request.user)
        return queryset


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Region creation, updation and deletion.
    GET without pk works only for staff users.
    All other operations require a pk to be supplied.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_queryset(self):
        queryset = Region.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PointInRegions(APIView):
    """
    Takes two URL parameters lng and lat and returns a list of regions containing them.
    The parameters are expected to be present in the URL.
    Returned data is a JSON array of region information.

    Example URL :-

    /regions/contains?lng=<value>&lat=<value>
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        parameters = request.query_params
        pnt = GEOSGeometry("POINT(%s %s)" % (parameters['lng'], parameters['lat']))
        result_set = Region.objects.filter(area__contains=pnt).values('name', 'creator__username', 'price')
        if result_set:
            return Response(list(result_set), status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_404_NOT_FOUND)

user_view = UserView.as_view({'get': 'list', 'post': 'create', })
user_detail = UserView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
region_list = RegionList.as_view()
region_detail = RegionDetail.as_view()
auth_view = AuthView.as_view()
point_in_region = PointInRegions.as_view()
