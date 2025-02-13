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
    #----log----

    path('turf_login/',views.turf_login,name='turf_login'), 
    path('turf_login1/', views.turf_login1, name='turf_login1'),

    path('turf_logout',views.turf_logout),
    
    
    path('register/', views.register, name='register'),


    #---admin----



    path('admin/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin/bookings', views.booking_list, name='admin_booking_list'),
    path('admin/turfs', views.turf_list, name='admin_turf_list'),




    #-----user-----




    path('', views.home, name='home'),
    path('booking/<int:turf_id>/', views.booking, name='booking'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]



