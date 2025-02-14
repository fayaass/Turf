from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os




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






from django.shortcuts import render ,  get_object_or_404, redirect
from .models import Turf
from .forms import TurfBookingForm

# View for booking slots
def booking_slots(request):
    if request.method == "POST":
        form = TurfBookingForm(request.POST)
        if form.is_valid():
            # Save the booking data
            form.save()
            # Redirect to the success page
            return redirect('booking_success')
    else:
        form = TurfBookingForm()
    
    return render(request, 'user/booking_slots.html', {'form': form})

# View for booking success
def booking_success(request):
    return render(request, 'user/booking_success.html')



from django.shortcuts import render, get_object_or_404, redirect
from .models import Turf

# View for listing all bookings
def view_bookings(request):
    bookings = Turf.objects.all()
    return render(request, 'user/view_bookings.html', {'bookings': bookings})

# View for deleting a booking
def delete_booking(request, pk):
    booking = get_object_or_404(Turf, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('view_bookings')  # Redirect to the booking list page after deletion

