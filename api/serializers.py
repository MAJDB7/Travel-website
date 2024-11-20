from rest_framework.serializers import ModelSerializer
from .utils import*
from .models import *


class HotelImagesSerializer(ModelSerializer):
    class Meta:
        model=HotelImages
        fields='__all__'
    
class HotelSerializer(ModelSerializer):
    H_photos=HotelImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = '__all__'

class ResturantSerializer(ModelSerializer):
    class Meta:
        model = Resturant
        fields = '__all__'

class TravelPlaceImagesSerializer(ModelSerializer):
    class Meta:
        model=TravelPlaceImages
        fields='__all__'
    
    
class TravelPlacesSerializer(ModelSerializer):
    hotels = HotelSerializer(many=True, read_only=True)
    photos = TravelPlaceImagesSerializer(many=True, read_only=True)
    resturants=ResturantSerializer(many=True,read_only=True)
    class Meta:
        model= TravelPlace
        fields='__all__'
    


    


class TouristSiteSerializer(ModelSerializer):
    class Meta:
        model = TouristSite
        fields = '__all__'



class AgencysSerializer(ModelSerializer):
    class Meta:
        model = Agencys
        fields = '__all__'

class TicketsSerializer(ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'