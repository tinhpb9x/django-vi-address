from rest_framework import serializers

from .models import City, District, Ward


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'


class CityDetailSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ('id', 'code', 'name', 'slug', 'type', 'name_with_type', 'districts')


class DistrictDetailSerializer(serializers.ModelSerializer):
    wards = WardSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = ('id', 'code', 'name', 'slug', 'type', 'name_with_type', 'path', 'path_with_type', 'wards')
