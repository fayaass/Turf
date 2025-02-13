from django.contrib import admin
from .models import Turf, Booking

class TurfAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price_per_hour', 'available_slots')
    search_fields = ('name', 'location')
    list_filter = ('location',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'turf', 'date', 'time_slot', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'turf__name')

admin.site.register(Turf, TurfAdmin)
admin.site.register(Booking, BookingAdmin)
