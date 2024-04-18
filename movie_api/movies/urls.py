# movie/urls.py
from django.urls import path
from .views import (
    MovieListCreateView,
    MovieRetrieveUpdateDestroyView,
    ShowtimeListCreateView,
    ShowtimeRetrieveUpdateDestroyView,
    TheaterListCreateView,
    TheaterRetrieveUpdateDestroyView,
    AvailableSeatsView,
    ReserveSeatsView,
    PurchaseTicketsView,
    RegisterView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    path('movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', MovieRetrieveUpdateDestroyView.as_view(), name='movie-retrieve-update-destroy'),
    path('theaters/', TheaterListCreateView.as_view(), name='theater-list-create'),
    path('theaters/<int:pk>/', TheaterRetrieveUpdateDestroyView.as_view(), name='theater-retrieve-update-destroy'),
    path('showtimes/', ShowtimeListCreateView.as_view(), name='showtime-list-create'),
    path('showtimes/<int:pk>/', ShowtimeRetrieveUpdateDestroyView.as_view(), name='showtime-retrieve-update-destroy'),
    path('showtimes/<int:pk>/seats/', AvailableSeatsView.as_view(), name='available-seats'),
    path('showtimes/<int:pk>/reserve/', ReserveSeatsView.as_view(), name='reserve-seats'),
    path('purchase-tickets/', PurchaseTicketsView.as_view(), name='purchase-tickets'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
