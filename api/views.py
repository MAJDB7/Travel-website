from django.db.models import Q,Case, When
from rest_framework.response import Response
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .models import *
from .utils import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from numpy import array
from datetime import date
# Create your views here.


# Recommendation Algorithm
def get_similar(place_id, rating, corrMatrix):
    similar_ratings = corrMatrix[place_id] * (rating - 2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def recommend(request):
#     # Fetch all ratings and create a DataFrame
#     place_rating = pd.DataFrame(list(Rating.objects.all().values()))

#     # Create user ratings pivot table
#     userRatings = place_rating.pivot_table(index=['user_id'], columns=['place_id'], values='value')
#     userRatings = userRatings.fillna(0)

#     # Compute the correlation matrix
#     corrMatrix = userRatings.corr(method='pearson')

#     # Fetch current user's ratings
#     user = pd.DataFrame(list(Rating.objects.filter(user=request.user).values())).drop(['user_id', 'id'], axis=1)
#     user_filtered = [tuple(x) for x in user.values]

#     # Get IDs of places already rated by the user
#     place_id_watched = [each[0] for each in user_filtered]

#     # Find similar places
#     similar_places = pd.DataFrame()
#     for place_id, rating in user_filtered:
#         similar_places = similar_places._append(get_similar(place_id, rating, corrMatrix))

#     # Sum up similarity scores and sort them
#     places_id = list(similar_places.sum().sort_values(ascending=False).index)
#     places_id_recommend = [each for each in places_id if each not in place_id_watched]

#     # Use Case and When to maintain the order of recommendations
#     preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(places_id_recommend)])

#     # Fetch the recommended travel places from the database
#     place_list = TravelPlace.objects.filter(id__in=places_id_recommend).order_by(preserved)[:10]

#     # Serialize the place list
#     serializer = TravelPlacesSerializer(place_list, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend(request):
    place_rating = pd.DataFrame(list(Rating.objects.all().values()))

    userRatings = place_rating.pivot_table(index=['user_id'], columns=['place_id'], values='value')
    userRatings = userRatings.fillna(0)

    corrMatrix = userRatings.corr(method='pearson')

    user = pd.DataFrame(list(Rating.objects.filter(user=request.user).values())).drop(['user_id', 'id'], axis=1)
    user_filtered = [tuple(x) for x in user.values]

    place_id_watched = [each[0] for each in user_filtered]

    similar_places = pd.DataFrame()
    for place_id, rating in user_filtered:
        similar_places = similar_places._append(get_similar(place_id, rating, corrMatrix))


    places_id = list(similar_places.sum().sort_values(ascending=False).index)
    places_id_recommend = [each for each in places_id if each not in place_id_watched]

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(places_id_recommend)])

    place_list = TravelPlace.objects.filter(id__in=places_id_recommend).order_by(preserved)[:10]
    serializer = TravelPlacesSerializer(place_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPLaces(request):
    travel=TravelPlace.objects.all()
    serializer=TravelPlacesSerializer(travel,many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def getPlace(request,pk):
    place=TravelPlace.objects.get(id=pk)
    serializer=TravelPlacesSerializer(place,many=False)
    return Response(serializer.data)

    
@api_view(['GET'])
def getSearch(request):
    query=request.query_params.get('q')
    if query is "":
        query="pppp"
        
    else:
        print('query : ',query)
        
    result=TravelPlace.objects.filter(Q(name__icontains=query)|Q(country__icontains=query))

    print(result)
    serializer=TravelPlacesSerializer(result,many=True)
    return Response(serializer.data)
    



@api_view(['GET'])
def getDate(request):
    query = request.query_params.get('q', None)
    
    if not query:  # If query is None or empty, return an error
        return Response({'status': 'No date provided'}, status=400)
    
    try:
        query_date = date.fromisoformat(query)
    except ValueError:
        return Response({'status': 'Invalid date format'}, status=400)
    
    if query_date < date.today():
        return Response({'status': 'Date cannot be from the past'}, status=400)
    
    # Fetch tickets with dates matching the query
    result = Ticket.objects.filter(date__icontains=query_date)
    serializer = TicketsSerializer(result, many=True)
    
    return Response(serializer.data, status=200)
@api_view(['GET'])
def getPrice(request):
    query=request.query_params.get('q')

    result=Ticket.objects.filter(price__lte=query)
    serializer=TicketsSerializer(result,many=True)
    return Response(serializer.data)

#for the tour site

@api_view(['GET'])
def getTourSites(request):
    sites = TouristSite.objects.all()
    serializer = TouristSiteSerializer(sites , many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTourSite(request,pk):
    site=TouristSite.objects.get(id=pk)
    serializer=TouristSiteSerializer(site,many=False)
    return Response(serializer.data)






#for the hotel

@api_view(['GET'])
def getHotels(request):
    hotels = Hotel.objects.all()
    serializer = HotelSerializer(hotels , many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getHotel(request,pk):
    hotel=Hotel.objects.get(id=pk)
    serializer=HotelSerializer(hotel,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getHotelSearch(request):
    query=request.query_params.get('q')
    if query is "":
        result=Hotel.objects.all()
        
    else:
        print('query : ',query)
        
    result=Hotel.objects.filter(city__icontains=query)

    print(result)
    serializer=HotelSerializer(result,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def getHotelFilters(request):
    H_type=request.data.get('H_type')
    station_dest=request.data.get('stations_dest')
    price=request.data.get('price')
    bed_num=request.data.get('bed_num')
    queryset = Hotel.objects.all()
    if H_type:
        queryset = queryset.filter(h_type=H_type)

    if station_dest:
        queryset = queryset.filter(stations_dest__lte=station_dest)

    if price:
        queryset = queryset.filter(price__lte=price)

    if bed_num:
        queryset = queryset.filter(bed_num__gte=bed_num)

    serializer=HotelSerializer(queryset,many=True)
    return Response(serializer.data)


#for the Agencys

@api_view(['GET'])
def getAgencys(request):
    airlines = Agencys.objects.all()
    serializer = AgencysSerializer(airlines , many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getAgency(request,pk):
    airline=Agencys.objects.get(id=pk)
    serializer=AgencysSerializer(airline,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getTickets(request,pk):
    ticket=Ticket.objects.filter(agency=pk)
    serializer=TicketsSerializer(ticket,many=True)
    return Response(serializer.data)


### resturant
@api_view(['GET'])
def getResturants(request):
    resturants = Resturant.objects.all()
    serializer = ResturantSerializer(resturants , many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getResturan(request,pk):
    resturant=Resturant.objects.get(id=pk)
    serializer=ResturantSerializer(resturant,many=False)
    return Response(serializer.data)


#for rating
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_place(request, pk):
    try:
        
        place = TravelPlace.objects.get(id=pk)
        user = request.user
        rating_value = int(request.data.get('rating'))
        if Rating.objects.all().values().filter(user=user,place=place):
            Rating.objects.all().values().filter(user=user,place=place).update(value=rating_value)
        else:
            rating = Rating.objects.create(user=user, place=place,value=rating_value)
            rating.save()
        
        
        return Response({'status': 'success'})
    except TravelPlace.DoesNotExist:
        return Response({'status': 'error', 'message': 'Place not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_rate_place(request,pk):
    place = TravelPlace.objects.get(id=pk)
    user=request.user
    finalResult =0
    if Rating.objects.all().values().filter(user=user,place=place):
        result=Rating.objects.get(user=user,place=place)
        serializer=RatingSerializer(result,many=False)
        finalResult = serializer.data
    
    return Response(finalResult)


@api_view(['POST'])
def upload_photo(request):
    if 'photo' not in request.FILES:
        return JsonResponse({'error': 'No photo provided'}, status=400)
    
    photo = request.FILES['photo']
    embedding = get_image_embedding(photo) 
    similar_places = find_similar_places(embedding) 
   
    order_conditions = [When(id=id, then=pos) for pos, id in enumerate(similar_places)]
    
    print(similar_places)
    

    travel_places_queryset = TravelPlace.objects.filter(photos__in=similar_places).order_by(Case(*order_conditions))
    
    serializer = TravelPlacesSerializer(travel_places_queryset, many=True)
    
    return JsonResponse({'suggested_places': serializer.data})
    
