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
        name = req.POST.get('name', '').strip()
        email = req.POST.get('email', '').strip()
        password = req.POST.get('password', '').strip()

        # Check if fields are empty
        if not name or not email or not password:
            messages.error(req, "All fields are required.")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(req, "User already exists.")
            return redirect('register')

        # Create and save user
        try:
            user = User.objects.create_user(username=email, first_name=name, email=email, password=password)
            user.save()
            messages.success(req, "Account created successfully! Please log in.")
            return redirect('shp_login')  # Ensure 'shp_login' is a valid route name
        except Exception as e:
            messages.error(req, f"Error: {str(e)}")
            return redirect('register')

    return render(req, 'user/register.html')


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



from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

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

        return HttpResponse('user/success.html')

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

