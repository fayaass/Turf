from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os

from .models import Booking, Turf
from django.contrib.auth.models import User
from django.contrib import messages




# from django.urls import reverse_lazy
# from django.contrib.auth.views import (
#     PasswordResetView, 
#     PasswordResetDoneView, 
#     PasswordResetConfirmView, 
#     PasswordResetCompleteView
# )

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'password_reset.html'
#     email_template_name = 'password_reset_email.html'
#     subject_template_name = 'password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')


# class CustomPasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'password_reset_done.html'

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')

# class CustomPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'password_reset_complete.html'





def shp_login(req):
    if 'trf' in req.session:
        return redirect(home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['trf']=uname   #create session
                return redirect(home)
            else:
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(shp_login)
    
    else:
        return render(req,'login.html')

def shp_login1(req):
    if 'trf' in req.session:
        return redirect(home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['trf']=uname   #create session
                return redirect(home)
            else:
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(shp_login)
    
    else:
        return render(req,'login.html')


def shp_home(request):
    return render(request, 'user/home.html')

def shp_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(shp_login)

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        # send_mail('user registration','eshop account created', settings.EMAIL_HOST_USER, [email])
        try:
           
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(shp_login)
        except:
            messages.warning(req,'User already exists.')
            return redirect(register)
    else:
        return render(req,'user/register.html')

#-------------------admin------------------------------------

def home(request):
    # Admin Dashboard
    total_bookings = Booking.objects.count()
    total_turfs = Turf.objects.count()
    return render(request, 'admin_dashboard.html', {
        'total_bookings': total_bookings,
        'total_turfs': total_turfs
    })


def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})

# def turf_list(request):
#     turfs = Turf.objects.all()
#     return render(request, 'turf_list.html', {'turfs': turfs})




#---------------------------user--------------------------

from django.shortcuts import render, get_object_or_404, redirect

from .models import Turf, Booking
from datetime import datetime

def user_home(request):
    turfs = Turf.objects.all()
    return render(request, 'user/user_home.html', {'turfs': turfs})









from django.shortcuts import render

def about(request):
    return render(request, 'user/about.html')  # Ensure about.html is inside your templates folder



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *



def contact(request):
    """Contact Page View"""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save contact form details to the database
        ContactForm.objects.create(name=name, email=email, message=message)

        return HttpResponse("<h2>Thank you for contacting us! We will get back to you soon.</h2>")

    return render(request, "user/contact.html")





from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Turfs,Bookings
from django.contrib import messages

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Turfs, Bookings

def book_turf(request):
    

    if request.method == 'POST':
        date = request.POST['date']
        time_slot = request.POST['time_slot']
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')

        # Check if the slot is available
        if Booking.objects.filter(date=date, time_slot=time_slot).exists():
            return render(request, 'user/book_turf.html', {'turf': turf, 'error': 'This time slot is already booked.'})

        # Save the booking
        booking = Bookings(

            date=date,
            time_slot=time_slot,
            customer_name=customer_name,
            customer_email=customer_email
        )
        

        return redirect('user/booking_success.html')  # Redirect after booking

    return render(request, 'user/book_turf.html')





def booking_success(request):
    return render(request, 'user/booking_success.html')
