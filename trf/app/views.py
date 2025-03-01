from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib import messages



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



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        if User.objects.filter(email=email).exists():
            messages.warning(req, "Email already registered")
            return redirect('register')
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        req.session['email'] = email
        req.session['name'] = name
        req.session['password'] = password
        send_mail(
            'Your OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP sent to your email")
        return redirect('verify_otp_reg')
    return render(req, 'user/register.html')

def verify_otp_reg(req):
    if req.method == 'POST':
        entered_otp = req.POST['otp'] 
        stored_otp = req.session.get('otp')
        email = req.session.get('email')
        name = req.session.get('name')
        password = req.session.get('password')
        if entered_otp == stored_otp:
            user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
            user.is_verified = True
            user.save()      
            messages.success(req, "Registration successful! You can now log in.")
            send_mail('User Registration Succesfull', 'Account Created Succesfully And Welcome To Bookmart', settings.EMAIL_HOST_USER, [email])
            return redirect('shp_login1')
        else:
            messages.warning(req, "Invalid OTP. Try again.")
            return redirect('verify_otp_reg')

    return render(req, 'verify_otp_reg.html')



#-------------------admin------------------------------------
from django.shortcuts import render, get_object_or_404, redirect


def home(request):
    
    return render(request, 'admin/home.html')



def booking_list(request):
    bookings = Turf.objects.all()
    return render(request, 'admin/booking_list.html', {'bookings': bookings})


# View for deleting a booking
def delete_booking_admin(request, pk):
    booking = get_object_or_404(Turf, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')  # Redirect to the booking list page after deletion


#---------------------------user--------------------------

def user_home(request):
    
    return render(request, 'user/user_home.html')



def about(request):
    return render(request, 'user/about.html')  # Ensure about.html is inside your templates folder



from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse

def contact(request):
    """Contact Page View - Sends Message to Admin Email"""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Email Subject & Message Body
        subject = f"New Contact Form Submission from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send Email
        send_mail(
            subject,
            message_body,
            "your-email@gmail.com",  # Sender (must match EMAIL_HOST_USER)
            ["muhammedfayas815@gmail.com"],  # Receiver (your email or admin email)
            fail_silently=False,
        )

        # Redirect to the success page after sending the email
        return redirect('success')  # Assuming you've defined a URL for the success page

    return render(request, "user/contact.html")








from django.shortcuts import render ,  get_object_or_404, redirect
from .models import Turf
from .forms import TurfBookingForm



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Turf  # Ensure you import your booking model
from .forms import TurfBookingForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Turf
from .forms import TurfBookingForm

@login_required  # Ensure only logged-in users can book
def booking_slots(request):
    if request.method == "POST":
        form = TurfBookingForm(request.POST)
        if form.is_valid():
            selected_slot = form.cleaned_data['date']  # Get selected date/time
            selected_game = form.cleaned_data['game']  # Get selected game

            # Check if the same date and time is already booked for the same sport
            if Turf.objects.filter(date=selected_slot, game=selected_game).exists():
                messages.error(request, "This slot is already booked for this sport. Please choose a different one.")
            else:
                booking = form.save(commit=False)  # Do not save immediately
                booking.user = request.user  # Assign the logged-in user
                booking.save()  # Save the booking
                messages.success(request, "Your slot has been successfully booked!")
                return redirect('booking_success')  # Redirect on success
    else:
        form = TurfBookingForm()
    
    return render(request, 'user/booking_slots.html', {'form': form})










# View for booking success
def booking_success(request):
    return render(request, 'user/booking_success.html')



from django.shortcuts import render, get_object_or_404, redirect
from .models import Turf

# View for listing all bookings
from django.contrib.auth.decorators import login_required

@login_required  # Ensure user is logged in
def view_bookings(request):
    bookings = Turf.objects.filter(user=request.user)  # Show only user's bookings
    return render(request, 'user/view_bookings.html', {'bookings': bookings})


# View for deleting a booking
def delete_booking(request, pk):
    booking = get_object_or_404(Turf, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('view_bookings')  # Redirect to the booking list page after deletion



def success(request):
    return render(request, 'user/success.html')





    from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string

# Mock function to simulate email sending for verification
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


