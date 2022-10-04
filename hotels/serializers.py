from rest_framework import serializers
from .models import Country, City, HotelFeature, HotelAmenity, HotelExtraFeature, Hotel


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'country']


class HotelFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelFeature
        fields = ['title', 'icon', 'is_active']


class HotelAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenity
        fields = ['title', 'icon', 'is_active']


class HotelExtraFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelExtraFeature
        fields = ['title', 'price']


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['title', 'locatedCity', 'startCount', 'description', 'features', 'amenities', 'extra_features']
