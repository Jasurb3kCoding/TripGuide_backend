from django.contrib import admin
from .models import Country, City, HotelFeature, HotelAmenity, HotelExtraFeature, Hotel, HotelImage, Review, \
    RoomFeature, Room, RoomImage


# Register your models here.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    fields = ['name', 'country']


@admin.register(HotelFeature)
class HotelFeatureAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'icon', 'is_active']


@admin.register(HotelAmenity)
class HotelAmenityAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'icon', 'is_active']


@admin.register(HotelExtraFeature)
class HotelExtraFeatureAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'price']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title', 'locatedCity', 'startCount', 'description', 'features', 'amenities', 'extra_features']


@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ['hotel']
    fields = ['hotel', 'image']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author']
    fields = ['parent',
              'author',
              'hotel',
              'message',
              'startCount',
              'created_date', ]


admin.site.register(RoomFeature)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['hotel',
              'title',
              'price',
              'features',
              'is_discount',
              'discount_rate', ]


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room']
    fields = ['image',
              'room',
              'order', ]
