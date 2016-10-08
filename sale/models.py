from django.db import models
from location import Location
import distance_module.distance_module import distance_km
# Create your models here.
# main sale model where the user can set the price of the book they are gonna
# sell


class Sale(models.Model):
    seller_id = models.CharField(max_length=500)
    seller_username = models.CharField(max_length=500)
    book = models.ForeignKey('search.Book')
    description = models.TextField()
    price = models.CharField(max_length=200)
    location = models.CharField(default='', max_length=255)
    geo_point = models.CharField(default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.seller_username)
        
    def getLocation(self):
        latitude, longitude = self.geo_point.split(',')
        return Location(latitude, longitude)
        
    def compareTo(self, otherSale, refLocation):
        selfLocation = self.getLocation()
        selfDistance = distance_km(refLocation.latitude,
                                    refLocation.longitude,
                                    selfLocation.latitude,
                                    selfLocation.longitude)
        otherDistance = distance_km(refLocation.latitude,
                                    refLocation.longitude,
                                    otherSale.getLocation().latitude,
                                    otherSale.getLocation().longitude)
        return selfDistance > otherDistance
    class Meta:
        ordering = ['-created_at']


# the below model is for user's who are interested in a sale
class SaleInterest(models.Model):
    interested_user_id = models.CharField(max_length=500)
    interested_username = models.CharField(max_length=500)
    sale = models.ForeignKey('Sale')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.interested_username)

    class Meta:
        ordering = ['-created_at']


class SaleImage(models.Model):
    sale = models.ForeignKey('Sale')
    img_type = models.CharField(default='', max_length='16')
    image_name = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_name


class SaleNotification(models.Model):
    ''' This is the main sale notification model to talk to the database'''
    notif_type = models.IntegerField()
    user_id = models.CharField(max_length='255')
    user_name = models.CharField(max_length='255')
    sale = models.ForeignKey('Sale')
    data = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.user_name
