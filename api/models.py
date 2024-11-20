from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TouristSite(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    story=models.TextField(max_length=200,null=True,blank=True)
    photo=models.ImageField(upload_to="places_ph",null=True,blank=True)

    def __str__(self):
        return self.name

class Agencys(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    poster=models.ImageField(upload_to="airlines_ph",null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    location=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name
    

class Ticket(models.Model):
    ECONOMY = 'E'
    BUSINESS = 'B'
    FIRST_CLASS = 'F'

    TICKET_TYPES = [
        (ECONOMY, 'Economy'),
        (BUSINESS, 'Business'),
        (FIRST_CLASS, 'First Class'),
    ]

    type = models.CharField(
        max_length=1,
        choices=TICKET_TYPES,
        default=ECONOMY,
        null=True,blank=True
    )
    
    destenation=models.CharField(max_length=50,null=True,blank=True)
    t_photo=models.ImageField(upload_to="ticket_ph",null=True,blank=True)
    price=models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    date=models.DateField(null=True,blank=True)
    agency=models.ManyToManyField(Agencys)
    def __str__(self):
        agencies = ', '.join([agency.name for agency in self.agency.all()])
        return f"{self.destenation} - {self.get_type_display()} - {agencies} "



class HotelImages(models.Model):
    h_name=models.CharField(max_length=50,null=True,blank=True)
    images=models.ImageField(upload_to="hotels_ph",null=True,blank=True)
    def __str__(self):
        return self.h_name
    
class Hotel(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    city=models.CharField(max_length=50,null=True,blank=True)
    h_type=models.CharField(max_length=50,null=True,blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)
    H_photo=models.ImageField(upload_to="hotels_ph",null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    size=models.IntegerField(null=True,blank=True)
    bed_num=models.IntegerField(null=True,blank=True)
    bathroom=models.IntegerField(null=True,blank=True)
    musuem_dest=models.IntegerField(null=True,blank=True)
    stations_dest=models.IntegerField(null=True,blank=True)
    resturant_dest=models.IntegerField(null=True,blank=True)
    rate=models.IntegerField(null=True,blank=True)
    latitude=models.DecimalField(max_digits=10,decimal_places=7,null=True,blank=True)
    longitude=models.DecimalField(max_digits=10,decimal_places=7,null=True,blank=True)
    H_photos=models.ManyToManyField(HotelImages)

    def __str__(self):
        return self.name

class Resturant(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    R_photo=models.ImageField(upload_to="resturants_ph",null=True,blank=True)
    rate=models.IntegerField(null=True,blank=True)
    city=models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.name

class TravelPlaceImages(models.Model):
    tp=models.CharField(max_length=50,null=True,blank=True)
    images=models.ImageField(upload_to="places_ph",null=True,blank=True)
    image_embedding = models.BinaryField(null=True,blank=True)

    def __str__(self):
        return self.tp

class TravelPlace(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    country=models.CharField(max_length=50,null=True,blank=True)
    story=models.TextField(max_length=200,null=True,blank=True)
    photo=models.ImageField(upload_to="places_ph",null=True,blank=True)
    photos=models.ManyToManyField(TravelPlaceImages)
    hotels=models.ManyToManyField(Hotel)
    resturants=models.ManyToManyField(Resturant)
    agencys=models.ManyToManyField(Agencys)
    image_embedding = models.BinaryField(null=True,blank=True)
    def __str__(self):
        return self.name
    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(TravelPlace, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return self.place.name 
    






