from django.urls import path
from . import views

urlpatterns=[

    path('api/',views.getPLaces,name="places"),
    path('search/',views.getSearch,name="Search"),
    path('date/',views.getDate,name="date"),
    path('place/<str:pk>',views.getPlace,name="place"),
  
    path('price/',views.getPrice,name="price"),

    path('sites/',views.getTourSites,name="getTourSites"),
    path('sites/<str:pk>',views.getTourSite,name="getTourSite"),


    path('hotels/',views.getHotels,name="getHotels"),
    path('hotels/<str:pk>',views.getHotel,name="getHotel"),
    path('hotel_search/',views.getHotelSearch,name="hotel_search"),
    path('filter_hotel_search/',views.getHotelFilters,name="filter_hotel_search"),

    path('rate/<str:pk>', views.rate_place, name='rate_place'),
    path('rateing/<str:pk>', views.get_rate_place,name='get_rate'),



    path('resturants/',views.getResturants,name="getResturants"),
    path('resturants/<str:pk>',views.getResturan,name="getResturan"),

    path('agencys/',views.getAgencys,name="getAgencys"),
    path('agency/<str:pk>',views.getAgency,name="getAgency"),
    path('tickets/<str:pk>',views.getTickets,name="getAgency"),
    # path('ticketss/<str:pk>',views.getTicketss,name="getAgency"),

    path('recommend/',views.recommend,name="recommend"),
    path('up_photo/',views.upload_photo,name="up_photo")
]