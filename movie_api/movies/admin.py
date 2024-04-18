from django.contrib import admin
from .models import Movie, Theater, Showtime, Reservation, Ticket

# Register your models here.
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Showtime)
admin.site.register(Reservation)
admin.site.register(Ticket)
