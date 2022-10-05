from django.db import models


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
    icon = models.CharField(max_length=50)
    is_active = models.BooleanField()

    def __str__(self):
        return self.title


class HotelAmenity(models.Model):
    title = models.CharField(max_length=250)
    icon = models.CharField(max_length=50)
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
