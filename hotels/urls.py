from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import city, country, hotel, hotelAmenity, hotelExtraFeature, hotelFeature

urlpatterns = [
    path('city/', city.CityList.as_view()),
    path('city/<int:pk>/', city.CityDetail.as_view()),
    path('country/', country.CountryList.as_view()),
    path('country/<int:pk>/', country.CountryDetail.as_view()),
    path('hotel/', hotel.HotelList.as_view()),
    path('hotel/<int:pk>/', hotel.HotelDetail.as_view()),
    path('hotel-amenity/', hotelAmenity.HotelAmenityList.as_view()),
    path('hotel-amenity/<int:pk>/', hotelAmenity.HotelAmenityDetail.as_view()),
    path('hotel-extra-feature/', hotelExtraFeature.HotelExtraFeatureList.as_view()),
    path('hotel-extra-feature/<int:pk>/', hotelExtraFeature.HotelExtraFeatureDetail.as_view()),
    path('hotel-feature/', hotelFeature.HotelFeatureList.as_view()),
    path('hotel-feature/<int:pk>/', hotelFeature.HotelFeatureDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
