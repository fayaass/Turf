from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.admin.views.decorators import staff_member_required
from .models import Booking, Turf
from django.contrib.auth.models import User
from django.contrib import messages




from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'






def turf_login(req):
    if 'watch' in req.session:
        return redirect(home)
    if 'user' in req.session:
        return redirect(home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['watch']=uname   #create session
                return redirect(admin_dashboard)
            else:
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(turf_login)
    
    else:
        return render(req,'login.html')
    

def turf_login1(req):
    if 'watch' in req.session:
        return redirect(admin_dashboard)
    if 'user' in req.session:
        return redirect(admin_dashboard)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['watch']=uname   #create session
                return redirect(admin_dashboard)
            else:
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(admin_dashboard)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(turf_login1)
    
    else:
        return render(req,'login.html')


def turf_logout(req):
    req.session.flush()          
    logout(req)
    return redirect(turf_login)



def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        # send_mail('user registration','watch account created', settings.EMAIL_HOST_USER, [email])
        try:
           
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(turf_login)
        except:
            messages.warning(req,'User already exists.')
            return redirect(register)
    else:
        return render(req,'user/register.html')



#-------------------admin------------------------------------

@staff_member_required
def admin_dashboard(request):
    # Admin Dashboard
    total_bookings = Booking.objects.count()
    total_turfs = Turf.objects.count()
    return render(request, 'admin_dashboard.html', {
        'total_bookings': total_bookings,
        'total_turfs': total_turfs
    })

@staff_member_required
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})

@staff_member_required
def turf_list(request):
    turfs = Turf.objects.all()
    return render(request, 'turf_list.html', {'turfs': turfs})




#---------------------------user--------------------------

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Turf, Booking
from datetime import datetime

def home(request):
    turfs = Turf.objects.all()
    return render(request, 'user/home.html', {'turfs': turfs})

def booking(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)
    if request.method == "POST":
        # Process the booking
        booking_date = request.POST['date']
        time_slot = request.POST['time_slot']

        # Create the booking
        booking = Booking(
            user=request.user,
            turf=turf,
            date=booking_date,
            time_slot=time_slot,
            status='Pending'
        )
        booking.save()

        # Redirect to booking confirmation page
        return redirect('booking_confirmation', booking_id=booking.id)
    
    return render(request, 'booking_page.html', {'turf': turf})

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})

@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'bookings': bookings})
