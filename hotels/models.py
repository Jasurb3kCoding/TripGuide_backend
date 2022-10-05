from django.db import models
from account.models import User


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HotelFeature(models.Model):
    title = models.CharField(max_length=250)
    icon = models.ImageField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.title


class HotelAmenity(models.Model):
    title = models.CharField(max_length=250)
    icon = models.ImageField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.title


class HotelExtraFeature(models.Model):
    title = models.CharField(max_length=250)
    price = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Hotel(models.Model):
    title = models.CharField(max_length=250)
    locatedCity = models.ForeignKey(City, on_delete=models.CASCADE)
    startCount = models.IntegerField()
    description = models.TextField()
    features = models.ForeignKey(HotelFeature, on_delete=models.CASCADE)
    amenities = models.ForeignKey(HotelAmenity, on_delete=models.CASCADE)
    extra_features = models.ForeignKey(HotelExtraFeature, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.hotel


class Review(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    message = models.TextField()
    startCount = models.IntegerField()
    created_date = models.DateTimeField()

    def __str__(self):
        return self.author


class RoomFeature(models.Model):
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    price = models.CharField(max_length=80)
    features = models.ForeignKey(RoomFeature, on_delete=models.CASCADE)
    is_discount = models.BooleanField()
    discount_rate = models.FloatField()

    def __str__(self):
        return self.title


class RoomImage(models.Model):
    image = models.ImageField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return self.room
