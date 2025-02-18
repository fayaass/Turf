from django.urls import path
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)



urlpatterns = [


    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('',views.shp_login, name='shp_login'),
    path('shp_login1/', views.shp_login1, name='shp_login1'),
    path('shp_logout/',views.shp_logout, name='shp_logout'),
    path('register/', views.register, name='register'),


    #---admin----



    path('home', views.home, name='home'),
    path('booking_list', views.booking_list, name='booking_list'),

    
    path('delete_booking_admin/<int:pk>/', views.delete_booking_admin, name='delete_booking_admin'),
    
   




    #-----user-----




    path('user_home/', views.user_home, name='user_home'),
    
   

    path('about/', views.about, name='about'),
    path("contact/", views.contact, name="contact"),
    


    path('booking_slots/', views.booking_slots, name='booking_slots'),
    path('booking_success/', views.booking_success, name='booking_success'),
   
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('delete_booking/<int:pk>/', views.delete_booking, name='delete_booking'),
    
    path('success/', views.success, name='success'),
]




