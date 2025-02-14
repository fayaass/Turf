from django.urls import path
from . import views



urlpatterns = [


    

    path('',views.shp_login, name='shp_login'),
    path('shp_login1/', views.shp_login1, name='shp_login1'),
    path('shp_logout',views.shp_logout),
    path('register/', views.register, name='register'),


    #---admin----



    path('home', views.home, name='home'),
    path('admin/bookings', views.booking_list, name='admin_booking_list'),
    # path('admin/turfs', views.turf_list, name='admin_turf_list'),




    #-----user-----




    path('user_home/', views.user_home, name='user_home'),
    
    path('book_turf/', views.book_turf, name='book_turf'),
    path('user/booking_success/', views.booking_success, name='booking_success'),
    path('about/', views.about, name='about'),

           
    path("contact/", views.contact, name="contact"),  # Contact Page
    # path("booking/", views.booking, name="booking"),  # Booking Page
    
]




