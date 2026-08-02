from rest_framework import serializers

from .models import City, Ward


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'


class CityDetailSerializer(serializers.ModelSerializer):
    wards = WardSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ('id', 'code', 'name', 'slug', 'type', 'name_with_type', 'wards')
