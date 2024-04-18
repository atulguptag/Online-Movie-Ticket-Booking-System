from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes
    synopsis = models.TextField()

    def __str__(self):
        return self.title

class Theater(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.movie.title} at {self.theater.name} on {self.date_and_time}"
    
class Reservation(models.Model):
    seats = models.CharField(max_length=100)  # Seats are stored as a comma-separated string like "A10, A11, A12"
    show = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    def __str__(self):
        return f"{self.user.username} reserving seat(s) {self.seats} for {str(self.show)}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} 's ticket to see {str(self.reservation.show.movie)}"
    

