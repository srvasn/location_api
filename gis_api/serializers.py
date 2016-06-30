from rest_framework import serializers as rest_serializers
from rest_framework_gis import serializers as gis_serializers
from django.contrib.auth.models import User

from gis_api.models import Region, Vendor


# __author__ = 'Sourav Banerjee'
# __email__ = ' srvasn@gmail.com'

class UserSerializer(rest_serializers.ModelSerializer):
    name = rest_serializers.CharField(source='profile.name', help_text='Name of the user')
    phone = rest_serializers.CharField(source='profile.phone', help_text='Phone number of the user')
    lang = rest_serializers.CharField(source='profile.lang', help_text='Language of communication')
    curr = rest_serializers.CharField(source='profile.curr', help_text='Currency preferred')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'phone', 'lang', 'curr', 'password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'locations', 'regions')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        print validated_data
        profile_data = validated_data.pop('profile')
        print profile_data
        user = User.objects.create_user(**validated_data)
        self.create_or_update_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        print profile_data
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        self.create_or_update_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = Vendor.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(UserSerializer, self).update(profile, profile_data)


class RegionSerializer(gis_serializers.GeoFeatureModelSerializer):
    creator = rest_serializers.ReadOnlyField(source='creator.username', help_text='Vendor who created the region')
    name = rest_serializers.CharField(max_length=255, help_text='Name of region')
    area = gis_serializers.GeometryField(help_text='GeoJSON polygon defining region')

    class Meta:
        model = Region
        geo_field = 'area'
        fields = ('id', 'uuid', 'name', 'price', 'creator')
