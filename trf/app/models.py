from django.db import models
from django.contrib.auth.models import User

class Turf(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    available_slots = models.IntegerField()

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Booking ID: {self.id} - {self.user.username}"



from django.db import models

class Turfs(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Bookings(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=5)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    
    def __str__(self):
        return f"{self.customer_name} - {self.turf.name} ({self.date} - {self.time_slot})"
